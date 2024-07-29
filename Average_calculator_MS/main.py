from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

WINDOW_SIZE = 10
numbers_window = []

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIyMjQyNzY0LCJpYXQiOjE3MjIyNDI0NjQsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjcwMGZiOTE1LTIxNTEtNDU2OC05YmFjLWY1NmRlNDJjMzczOSIsInN1YiI6InNoYWhzd2F0c2hhcm1hMTIzMDRAZ21haWwuY29tIn0sImNvbXBhbnlOYW1lIjoiQW1pdHkgVW5pdmVyc2l0eSBVdHRhciBQcmFkZXNoIiwiY2xpZW50SUQiOiI3MDBmYjkxNS0yMTUxLTQ1NjgtOWJhYy1mNTZkZTQyYzM3MzkiLCJjbGllbnRTZWNyZXQiOiJFaE9mSHVWU0djTFh3aUJGIiwib3duZXJOYW1lIjoiU2hhc2h3YXQgU2hhcm1hIiwib3duZXJFbWFpbCI6InNoYWhzd2F0c2hhcm1hMTIzMDRAZ21haWwuY29tIiwicm9sbE5vIjoiQTIzMDUzMjEwNDMifQ.iw6_FZ1VoUD9A39CjNM2_ZIH1YsmXmAUeuPlEEVdpJo"

class ResponseModel(BaseModel):
    windowPrevState: List[int]
    windowCurrState: List[int]
    numbers: List[int]
    avg: float

def fetch_numbers(number_id: str) -> List[int]:
    urls = {
        "p": "http://20.244.56.144/test/primes",
        "f": "http://20.244.56.144/test/fibo",
        "e": "http://20.244.56.144/test/even",
        "r": "http://20.244.56.144/test/rand"
    }
    
    url = urls.get(number_id)
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=0.5)
        response.raise_for_status()
        numbers = response.json().get("numbers", [])
        return numbers
    except requests.Timeout:
        print(f"Timeout occurred while fetching numbers for ID: {number_id}")
        return []
    except requests.RequestException as e:
        print(f"RequestException occurred: {e}")
        return []
    except ValueError as e:
        print(f"ValueError occurred: {e}")
        return []

def calculate_average(numbers: List[int]) -> float:
    if len(numbers) == 0:
        return 0.0
    return sum(numbers) / len(numbers)

@app.get("/numbers/{number_id}", response_model=ResponseModel)
def get_numbers(number_id: str):
    if number_id not in ["p", "f", "e", "r"]:
        raise HTTPException(status_code=400, detail="Invalid number ID")

    new_numbers = fetch_numbers(number_id)

    if not new_numbers:
        raise HTTPException(status_code=500, detail="Failed to fetch numbers")

    window_prev_state = numbers_window.copy()

    for num in new_numbers:
        if num not in numbers_window:
            if len(numbers_window) >= WINDOW_SIZE:
                numbers_window.pop(0)
            numbers_window.append(num)

    avg = calculate_average(numbers_window)

    response = ResponseModel(
        windowPrevState=window_prev_state,
        windowCurrState=numbers_window.copy(),
        numbers=new_numbers,
        avg=round(avg, 2)
    )

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9876)