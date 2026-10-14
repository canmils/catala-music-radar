import tempfile, os, unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
from src import musicbrainz_collector as collector
class CollectorTest(unittest.TestCase):
    def test_csv_from_a_mocked_source_and_empty_input(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); artists=root/"artists.txt";artists.write_text("Fictional Artist\n")
            with patch.object(collector,"ARTISTS_FILE",artists),patch.object(collector,"OUTPUT_DIR",root),patch.object(collector,"search_artist",return_value={"name":"Fictional Artist","id":"demo"}),patch.object(collector,"get_releases",return_value=[{"title":"Fictional EP","first-release-date":date.today().isoformat(),"primary-type":"EP"}]),patch.object(collector.time,"sleep"):
                collector.main()
                files=list(root.glob("musicbrainz_recent_*.csv"))
                self.assertEqual(len(files),1)
                self.assertIn("Fictional EP",files[0].read_text(encoding="utf-8-sig"))
                artists.write_text("")
                collector.main()
if __name__=="__main__":unittest.main()
