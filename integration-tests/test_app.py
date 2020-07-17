import pytest
from datetime import dateime

@pytest.fixture()
def mock_trello_get_requests(monkeypatch, id, name, date: dateime):
    def mock_trello_return(*args, **kwargs):
        return {
            {
                'id': id,
                'checkItemStates': None,
                'closed': False,
                'dateLastActivity': f'{date.isoformat()}Z',
                'desc': '',
                'descData': None,
                'dueReminder': None,
                'idBoard': '5eeb34b895d54b77a6a7b8fa',
                'idList': '5eeb34b895d54b77a6a7b8fd',
                'idMembersVoted': [],
                'idShort': 9,
                'idAttachmentCover': None,
                'idLabels': [],
                'manualCoverAttachment': False,
                'name': name,
                'pos': 147455,
                'shortLink': '6NOVODOY',
                'isTemplate': False,
                'badges': {
                    'attachmentsByType': {
                        'trello': {
                            'board': 0,
                            'card': 0
                        }
                    },
                    'location': False,
                    'votes': 0,
                    'viewingMemberVoted': False,
                    'subscribed': False,
                    'fogbugz': '',
                    'checkItems': 0,
                    'checkItemsChecked': 0,
                    'checkItemsEarliestDue': None,
                    'comments': 0,
                    'attachments': 0,
                    'description': False,
                    'due': None,
                    'dueComplete': False
                },
                'dueComplete': False,
                'due': None,
                'idChecklists': [],
                'idMembers': [],
                'labels': [],
                'shortUrl': 'https://trello.com/c/6NOVODOY',
                'subscribed': False,
                'url': 'https://trello.com/c/6NOVODOY/9-dsad',
                'cover': {
                    'idAttachment': None,
                    'color': None,
                    'idUploadedBackground': None,
                    'size': 'normal',
                    'brightness': 'light'
                }
            }
        }
    monkeypatch.setattr(view_model, "_today", mock_today)

def test_index_page(mock_get_requests, client):
    response = client.get('/')
    print(response)