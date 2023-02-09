from locust import HttpUser, task,between

class AppUser(HttpUser):
    wait_time = between(2, 5)

    @task
    def test_index(self):
        self.client.get("/")

    @task
    def test_showSummary(self):
        from_data = {'email':'admin@irontemple.com'}
        self.client.post("/showSummary", data = from_data)

    @task
    def test_book(self):
        self.client.get("/book/atam competiton/She Lifts")

    @task
    def test_purchasePlaces(self):
        from_data = {'competition': 'atam competiton',
                'club': 'Simply Lift',
                'date': '2023-03-30 13:30:00',
                'places':'10'}
        self.client.post("/purchasePlaces", data = from_data)

    @task
    def test_images(self):
        self.client.get("/images/stade_bg.png")
    
    @task
    def test_logout(self):
        self.client.get("/logout")