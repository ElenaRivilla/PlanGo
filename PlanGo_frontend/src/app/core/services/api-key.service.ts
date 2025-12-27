import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { globals } from '../globals';


@Injectable({ providedIn: 'root' })
export class ApiKeyService {
  constructor(
    private httpClient: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  getGooglePlacesApiKey() {
    let token = '';
    if (isPlatformBrowser(this.platformId)) {
      token = localStorage.getItem('authToken') || '';
    }
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
    return this.httpClient.get<{ googlePlacesApiKey: string }>(`${globals.apiBaseUrl}/api/google-places-key/`, { headers } );
  }
}