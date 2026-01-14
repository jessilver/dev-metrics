#!/usr/bin/env python3
"""
Script para gerar métricas de desenvolvimento do GitHub.
Analisa PRs de repositórios específicos e calcula métricas de produtividade e qualidade.
"""

import os
import sys
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
from dateutil import parser
from github import Github, GithubException
from github.PullRequest import PullRequest
from github.Repository import Repository


class MetricsCalculator:
    """Calcula métricas de desenvolvimento a partir de PRs do GitHub."""
    
    def __init__(self, token: str, author: str):
        """
        Inicializa o calculador de métricas.
        
        Args:
            token: Token de autenticação do GitHub
            author: Username do autor para filtrar PRs
        """
        self.github = Github(token)
        self.author = author
    
    def get_merged_prs(self, repo: Repository) -> List[PullRequest]:
        """
        Obtém PRs merged do autor especificado.
        
        Args:
            repo: Repositório do GitHub
            
        Returns:
            Lista de pull requests merged
        """
        try:
            pulls = repo.get_pulls(state='closed', sort='created', direction='desc')
            merged_prs = []
            
            for pr in pulls:
                if pr.merged and pr.user.login == self.author:
                    merged_prs.append(pr)
            
            return merged_prs
        except GithubException as e:
            print(f"Erro ao obter PRs: {e}")
            return []
    
    def get_pr_commits(self, pr: PullRequest) -> List:
        """
        Obtém commits de um PR.
        
        Args:
            pr: Pull request
            
        Returns:
            Lista de commits
        """
        try:
            return list(pr.get_commits())
        except GithubException:
            return []
    
    def calculate_coding_time(self, commits: List) -> Optional[float]:
        """
        Calcula tempo entre primeiro e último commit (em horas).
        
        Args:
            commits: Lista de commits do PR
            
        Returns:
            Tempo de codificação em horas ou None se não houver commits suficientes
        """
        if len(commits) < 2:
            return None
        
        first_commit_date = commits[0].commit.author.date
        last_commit_date = commits[-1].commit.author.date
        
        delta = last_commit_date - first_commit_date
        return delta.total_seconds() / 3600  # Converter para horas
    
    def calculate_commit_interval(self, commits: List) -> Optional[float]:
        """
        Calcula intervalo médio entre commits consecutivos (em horas).
        
        Args:
            commits: Lista de commits do PR
            
        Returns:
            Intervalo médio em horas ou None se não houver commits suficientes
        """
        if len(commits) < 2:
            return None
        
        intervals = []
        for i in range(1, len(commits)):
            prev_date = commits[i-1].commit.author.date
            curr_date = commits[i].commit.author.date
            interval = (curr_date - prev_date).total_seconds() / 3600
            intervals.append(interval)
        
        return sum(intervals) / len(intervals) if intervals else None
    
    def calculate_cycle_time(self, pr: PullRequest) -> Optional[float]:
        """
        Calcula tempo total do PR (criação até merge) em horas.
        
        Args:
            pr: Pull request
            
        Returns:
            Cycle time em horas ou None se PR não foi merged
        """
        if not pr.merged_at:
            return None
        
        delta = pr.merged_at - pr.created_at
        return delta.total_seconds() / 3600
    
    def calculate_flow_efficiency(self, coding_time: Optional[float], 
                                  cycle_time: Optional[float]) -> Optional[float]:
        """
        Calcula flow efficiency (%).
        
        Args:
            coding_time: Tempo de codificação em horas
            cycle_time: Tempo total do ciclo em horas
            
        Returns:
            Flow efficiency em porcentagem ou None se não for possível calcular
        """
        if coding_time is None or cycle_time is None or cycle_time == 0:
            return None
        
        return (coding_time / cycle_time) * 100
    
    def get_release_prs(self, repo: Repository) -> List[PullRequest]:
        """
        Identifica PRs de release (merge de release/* para main).
        
        Args:
            repo: Repositório do GitHub
            
        Returns:
            Lista de PRs de release
        """
        try:
            pulls = repo.get_pulls(state='closed', base='main', sort='created', direction='desc')
            release_prs = []
            
            for pr in pulls:
                if pr.merged and pr.head.ref.startswith('release'):
                    release_prs.append(pr)
            
            return release_prs
        except GithubException as e:
            print(f"Erro ao obter release PRs: {e}")
            return []
    
    def get_release_tags(self, repo: Repository) -> List:
        """
        Obtém tags de release do repositório.
        
        Args:
            repo: Repositório do GitHub
            
        Returns:
            Lista de tags
        """
        try:
            return list(repo.get_tags())
        except GithubException as e:
            print(f"Erro ao obter tags: {e}")
            return []
    
    def calculate_lead_time(self, pr: PullRequest, release_prs: List[PullRequest], 
                           tags: List) -> Optional[float]:
        """
        Calcula lead time até deploy (em horas).
        
        Args:
            pr: Pull request
            release_prs: Lista de PRs de release
            tags: Lista de tags de release
            
        Returns:
            Lead time em horas ou None se não houver deploy identificado
        """
        if not pr.merged_at:
            return None
        
        # Procurar o primeiro deploy após o merge do PR
        deploy_date = None
        
        # Verificar release PRs
        for release_pr in release_prs:
            if release_pr.merged_at and release_pr.merged_at > pr.merged_at:
                if deploy_date is None or release_pr.merged_at < deploy_date:
                    deploy_date = release_pr.merged_at
        
        # Verificar tags
        for tag in tags:
            try:
                tag_commit = tag.commit
                if hasattr(tag_commit, 'commit'):
                    tag_date = tag_commit.commit.author.date
                    if tag_date > pr.merged_at:
                        if deploy_date is None or tag_date < deploy_date:
                            deploy_date = tag_date
            except:
                continue
        
        if deploy_date:
            delta = deploy_date - pr.created_at
            return delta.total_seconds() / 3600
        
        return None
    
    def is_failed_deployment(self, pr: PullRequest) -> bool:
        """
        Verifica se um PR representa um deployment que falhou.
        
        Args:
            pr: Pull request
            
        Returns:
            True se for um deployment que falhou
        """
        # Verificar labels
        label_names = [label.name.lower() for label in pr.labels]
        failure_indicators = ['bug', 'hotfix', 'revert']
        
        return any(indicator in label_names for indicator in failure_indicators)
    
    def calculate_cfr(self, prs: List[PullRequest]) -> float:
        """
        Calcula Change Failure Rate (%).
        
        Args:
            prs: Lista de pull requests
            
        Returns:
            CFR em porcentagem
        """
        if not prs:
            return 0.0
        
        failed_count = sum(1 for pr in prs if self.is_failed_deployment(pr))
        return (failed_count / len(prs)) * 100
    
    def analyze_repository(self, repo_name: str) -> Dict:
        """
        Analisa um repositório e calcula todas as métricas.
        
        Args:
            repo_name: Nome do repositório (owner/repo)
            
        Returns:
            Dicionário com as métricas calculadas
        """
        print(f"\n--- Processando repositório: {repo_name} ---")
        
        try:
            repo = self.github.get_repo(repo_name)
        except GithubException as e:
            print(f"Erro ao acessar repositório {repo_name}: {e}")
            return {}
        
        # Obter PRs merged do autor
        prs = self.get_merged_prs(repo)
        print(f"PRs contabilizados: {len(prs)}")
        
        if not prs:
            print("Nenhum PR encontrado para análise.")
            return {}
        
        # Coletar dados para cálculo de métricas
        coding_times = []
        commit_intervals = []
        cycle_times = []
        flow_efficiencies = []
        lead_times = []
        
        # Obter informações de deploys
        release_prs = self.get_release_prs(repo)
        tags = self.get_release_tags(repo)
        
        for pr in prs:
            commits = self.get_pr_commits(pr)
            
            # Tempo de codificação
            coding_time = self.calculate_coding_time(commits)
            if coding_time is not None:
                coding_times.append(coding_time)
            
            # Intervalo entre commits
            commit_interval = self.calculate_commit_interval(commits)
            if commit_interval is not None:
                commit_intervals.append(commit_interval)
            
            # Cycle time
            cycle_time = self.calculate_cycle_time(pr)
            if cycle_time is not None:
                cycle_times.append(cycle_time)
            
            # Flow efficiency
            flow_eff = self.calculate_flow_efficiency(coding_time, cycle_time)
            if flow_eff is not None:
                flow_efficiencies.append(flow_eff)
            
            # Lead time
            lead_time = self.calculate_lead_time(pr, release_prs, tags)
            if lead_time is not None:
                lead_times.append(lead_time)
        
        # Calcular médias
        metrics = {
            'repo_name': repo_name,
            'pr_count': len(prs),
            'avg_coding_time': sum(coding_times) / len(coding_times) if coding_times else 0,
            'avg_commit_interval': sum(commit_intervals) / len(commit_intervals) if commit_intervals else 0,
            'avg_cycle_time': sum(cycle_times) / len(cycle_times) if cycle_times else 0,
            'avg_flow_efficiency': sum(flow_efficiencies) / len(flow_efficiencies) if flow_efficiencies else 0,
            'avg_lead_time': sum(lead_times) / len(lead_times) if lead_times else 0,
            'cfr': self.calculate_cfr(prs)
        }
        
        return metrics
    
    def print_metrics(self, metrics: Dict):
        """
        Imprime as métricas em formato legível.
        
        Args:
            metrics: Dicionário com as métricas calculadas
        """
        if not metrics:
            return
        
        print("----------------------------------------")
        print("MÉTRICAS DE DESENVOLVIMENTO:")
        print(f"Média Tempo Codificando:     {metrics['avg_coding_time']:.2f} h")
        print(f"Média Intervalo entre Commits: {metrics['avg_commit_interval']:.2f} h")
        print(f"Média Tempo Total (Cycle):   {metrics['avg_cycle_time']:.2f} h")
        print(f"Flow Efficiency (Tarefa):    {metrics['avg_flow_efficiency']:.2f}%")
        print("----------------------------------------")
        print("MÉTRICAS DE QUALIDADE E ENTREGA:")
        print(f"Lead time médio (até deploy): {metrics['avg_lead_time']:.2f} h")
        print(f"Change Failure Rate (CFR):    {metrics['cfr']:.2f}%")
        print("----------------------------------------\n")


def main():
    """Função principal para executar a análise de métricas."""
    # Obter token de ambiente
    token = os.getenv('GITHUB_TOKEN') or os.getenv('METRICS_TOKEN')
    if not token:
        print("Erro: Token do GitHub não encontrado.")
        print("Configure a variável de ambiente GITHUB_TOKEN ou METRICS_TOKEN")
        sys.exit(1)
    
    # Autor para filtrar PRs
    author = 'jessilver'
    
    # Repositórios para analisar
    repositories = [
        'MellloJ/Inclusiv',
        'Coutinhopmw/awtkd_django'
    ]
    
    print("=" * 50)
    print("Métricas de desenvolvimento")
    print("=" * 50)
    
    # Criar calculador de métricas
    calculator = MetricsCalculator(token, author)
    
    # Analisar cada repositório
    all_metrics = []
    for repo_name in repositories:
        try:
            metrics = calculator.analyze_repository(repo_name)
            if metrics:
                calculator.print_metrics(metrics)
                all_metrics.append(metrics)
        except Exception as e:
            print(f"Erro ao processar {repo_name}: {e}")
            continue
    
    print("=" * 50)
    print(f"Análise concluída. Total de repositórios processados: {len(all_metrics)}")
    print("=" * 50)


if __name__ == '__main__':
    main()
