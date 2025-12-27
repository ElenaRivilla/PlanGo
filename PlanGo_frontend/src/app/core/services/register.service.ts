import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { globals } from '../../core/globals';

@Injectable({
  providedIn: 'root',
})
export class RegisterService {
  constructor(private http: HttpClient) {}

private createHeaders(idToken: string): HttpHeaders {
    return new HttpHeaders({
        Authorization: `Bearer ${idToken}`,
        'Content-Type': 'application/json',
    });
}

  registerUser(idToken: string, payload: { email: string; first_name: string; last_name: string }): Observable<any> {
    const headers = this.createHeaders(idToken);
    return this.http.post(`${globals.apiBaseUrl}/users/register/`, { payload }, { headers });
  }
}