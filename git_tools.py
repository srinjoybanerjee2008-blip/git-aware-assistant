from git import Repo
from pathlib import Path
from typing import Optional

class GitTools:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)
        self.repo_path = Path(repo_path)

    def git_diff(self, ref_a: str = 'HEAD~1', ref_b: str = 'HEAD', path: Optional[str] = None) -> str:
        try:
            a = self.repo.commit(ref_a)
            b = self.repo.commit(ref_b)
        except Exception as e:
            return f'Error resolving commits: {e}'
        diffs = a.diff(b, paths=path)
        out = []
        for d in diffs:
            # d.a_path, d.b_path, d.diff is bytes-like in some versions
            info = {
                'a_path': d.a_path,
                'b_path': d.b_path,
                'change_type': d.change_type
            }
            try:
                diff_text = d.diff.decode('utf-8', errors='replace')
            except Exception:
                diff_text = str(d.diff)
            out.append(f"--- FILE: {d.b_path or d.a_path} | change: {d.change_type}\n" + diff_text)
        return '\n'.join(out) if out else 'No diff.'

    def blame_file(self, path: str, lineno: Optional[int] = None):
        # returns git blame info for the file using subprocess for line-porcelain
        import subprocess
        cmd = ['git','-C',str(self.repo_path), 'blame', '--line-porcelain', str(path)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.stdout if res.returncode == 0 else res.stderr

    def recent_commits(self, n=20):
        return list(self.repo.iter_commits(max_count=n))
