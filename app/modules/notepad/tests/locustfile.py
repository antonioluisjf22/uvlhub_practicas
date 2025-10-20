from locust import HttpUser, TaskSet, task
from core.environment.host import get_host_for_locust_testing


class NotepadBehavior(TaskSet):
    def on_start(self):
        self.index()

    @task(1)
    def index(self):
        response = self.client.get("/notepad")

        if response.status_code != 200:
            print(f"Notepad index failed: {response.status_code}")

    @task(2)
    def create_notepad(self):
        response = self.client.post("/notepad/create", data={
            "title": "Load Test Notepad",
            "body": "This is a notepad created during LOCUST load testing."
        })

        if response.status_code != 200:
            print(f"Notepad creation failed: {response.status_code}")
        else:
            print("Notepad created successfully during load test.")

class NotepadUser(HttpUser):
    tasks = [NotepadBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
