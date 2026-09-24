import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from feedback_quality_evaluator.core import score_feedback

result=score_feedback('Revise the claim because the evidence does not support it.', True)
for key,value in result.items():
    print(f"{key.replace('_',' ').title()}: {value}")
