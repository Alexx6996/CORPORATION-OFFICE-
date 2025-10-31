def test_smoke_basic():
    # базовый sanity-check для pytest, чтобы мы знали что окружение живёт
    assert 2 + 2 == 4

def test_http_mock_example(http_mock):
    # демонстрация того, что внешние вызовы должны быть моканы
    http_mock.get('https://ext.example/api/info', json={'status': 'ok', 'service': 'aioffice'}, status_code=200)

    import requests
    resp = requests.get('https://ext.example/api/info')
    assert resp.status_code == 200
    data = resp.json()
    assert data['service'] == 'aioffice'
