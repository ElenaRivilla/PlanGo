import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { globals } from '../globals';
import { BaseHttpService } from './base-http.service';
import { MessageService } from '../messageService';

@Injectable({
  providedIn: 'root',
})
export class LoginService extends BaseHttpService {
  constructor(
    public override httpClient: HttpClient, 
    @Inject(PLATFORM_ID) private platformId: Object,
    public override toast: MessageService 
  ) {
    super(httpClient, toast); 
  }

  private createHeaders(): HttpHeaders {
    let token = '';
    if (isPlatformBrowser(this.platformId)) {
      token = localStorage.getItem(globals.keys.accessToken) || '';
    }

    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
  }

  loginWithGoogle(idToken: string): Observable<any> {
    const headers = this.createHeaders();
    return this.httpClient.post(`${globals.apiBaseUrl}/users/login-with-google/`, {}, { headers });
  }

  loginWithEmail(idToken: string): Observable<any> {
    const headers = this.createHeaders();
    const body = { idToken }; // Incluye el token en el cuerpo
    return this.httpClient.post(`${globals.apiBaseUrl}/users/login-with-email/`, body, { headers });
  }
}