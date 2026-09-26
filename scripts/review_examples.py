"""Reproduce the labeled worked example; this is not an empirical study."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from feedback_quality_evaluator import core
outputs={'Cohen kappa: [1,1,0] vs [1,0,0]': core.cohen_kappa([1,1,0],[1,0,0]), 'constant-label kappa': core.cohen_kappa([1,1],[1,1]), 'exact agreement of constant labels': core.exact_agreement([1,1],[1,1])}
result={'kind':'illustrative_calculation','note':'Worked rating examples; undefined kappa is shown explicitly.','outputs':outputs}
(ROOT/'results/review_examples.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
