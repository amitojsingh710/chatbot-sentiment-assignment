import os
from app.storage import ConversationStorage

def test_add_and_save(tmp_path):
    file = tmp_path / "test.json"
    storage = ConversationStorage(file_path=str(file))
    storage.add_message("User", "Hello", "Good")
    storage.save()
    assert os.path.exists(file)
    assert "Hello" in open(file).read()
