import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map, Observable, throwError } from 'rxjs';
import { globals } from '../globals';
import { BaseHttpService } from './base-http.service';
import { MessageService } from '../messageService';

@Injectable({
  providedIn: 'root',
})
export class UserService extends BaseHttpService {
    private csrfToken: string = '';
    
  constructor(
    public override httpClient: HttpClient, 
    @Inject(PLATFORM_ID) private platformId: Object,
    public override toast: MessageService 
  ) {
    super(httpClient, toast); 
  }

  getUserById(userId: number): Observable<any> {
    let headers = this.createHeaders();
    return this.httpClient.get(`${globals.apiBaseUrl}/users/${userId}/`, { headers, withCredentials: true });
    }

 private createHeaders(): HttpHeaders {
    let token = '';
    if (isPlatformBrowser(this.platformId)) {
      token = localStorage.getItem(globals.keys.accessToken) || '';
    }
  
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
      'X-CSRFToken': this.csrfToken,
      'Content-Type': 'application/json',
    });
  }

  getCsrfTokenFromServer(): Observable<string> {
      if (!isPlatformBrowser(this.platformId)) return throwError(() => new Error('localStorage is not available in this environment'));
  
      const token = localStorage.getItem(globals.keys.accessToken) || '';
      if (!token) {
        return throwError(() => new Error('Token de usuario no disponible'));
      }
  
      const headers = new HttpHeaders({
        Authorization: `Bearer ${token}`,
      });
  
      return this.httpClient.get<{ csrftoken: string }>(`${globals.apiBaseUrl}/itineraries/csrf-token/`, {
        headers,
        withCredentials: true, 
      }).pipe(
        map((response) => response.csrftoken)
      );
    }
  
    setCsrfToken(token: string): void {
      this.csrfToken = token.replace(/^"|"$/g, '');
    }
}
