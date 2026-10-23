"""Local-only OMEGA fixture; no remote engine, provider or clinical claim."""
from pathlib import Path
import argparse,hashlib,json,sys
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args(); dest=args.output.absolute()
    if dest.exists() or dest.is_symlink() or not dest.parent.is_dir():
        ap.error('Output must be a new directory with an existing parent')
    if any(p.is_symlink() for p in dest.parents):ap.error('Symlinked output parents forbidden')
    sys.path[:0]=[str(ROOT/'source'),str(ROOT/'source/reference')]
    import omega_common as common
    common.PKG=ROOT/'source';common.PROTOCOL=common.PKG/'OMEGA_PROTOCOL.json'
    common.ROOT=dest;common.PYTHON=Path(sys.executable)
    import omega_synth as synth
    from omega_localfleet import LocalFleet
    from reference.rari_neurobrain.world import Bank
    dest.mkdir(mode=0o700)
    key=hashlib.sha256(common.protocol()['synthetic']['seed_label'].encode()).digest()
    row=synth._direct_probe(LocalFleet(),Bank(key),'closed_test',2080,'balanced',0)
    common.write(dest/'fixture.json',row)
    receipt={'status':'PASS','mode':'single-preserved-fixture','family':row['family'],
      'clinical_validation':False,'full_campaign_replay':False,'provider_calls':0,
      'fixture_sha256':common.sha(dest/'fixture.json')}
    common.write(dest/'RUN_RECEIPT.json',receipt);print(json.dumps(receipt))
    return 0
if __name__=='__main__':raise SystemExit(main())
