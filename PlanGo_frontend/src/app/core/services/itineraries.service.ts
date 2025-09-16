import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map, Observable, switchMap, throwError, of } from 'rxjs';
import { globals } from '../globals';
import { BaseHttpService } from './base-http.service';
import { MessageService } from '../messageService';
import { user } from '@angular/fire/auth';
import { Itinerary } from '../../itineraries/interfaces/itinerary.interface';

@Injectable({
  providedIn: 'root',
})
export class ItinerariesService extends BaseHttpService {
  private csrfToken: string = '';

  constructor(
    public override httpClient: HttpClient, 
    @Inject(PLATFORM_ID) private platformId: Object,
    public override toast: MessageService 
  ) {
    super(httpClient, toast); 
  }

  getItineraries(): Observable<any> {
    return this.getIdUser().pipe(
      switchMap((userId) => {
        if (userId === null) return of({ itineraries: [] });
        const headers = this.createHeaders();
        return this.httpClient.get(`${globals.apiBaseUrl}/itineraries/itinerary/user/${userId}/`, { headers });
      })
    );
  }

  getItineraryById(itineraryId: number): Observable<any> {
    const headers = this.createHeaders();
    return this.httpClient.get(`${globals.apiBaseUrl}/itineraries/itinerary/${itineraryId}/`, { headers });
  }
  
  createItinerary(itinerary: Itinerary): Observable<any> {
    const headers = this.createHeaders();
    return this.httpClient.post(`${globals.apiBaseUrl}/itineraries/itinerary/create/`, itinerary, {
      headers,
      withCredentials: true, 
    });
  }
  
  getIdUser(): Observable<number | null> {
    if (!isPlatformBrowser(this.platformId)) return of(null);

    const token = localStorage.getItem(globals.keys.accessToken) || '';
    if (!token) return throwError(() => new Error('No token found in localStorage'));

    const payloadBase64 = token.split('.')[1];
    if (!payloadBase64) return throwError(() => new Error('Invalid token format'));

    const decodedPayload = JSON.parse(atob(payloadBase64));
    const uid = decodedPayload?.uid || decodedPayload?.sub;
    if (!uid) return throwError(() => new Error('UID not found in token'));

    const headers = this.createHeaders();
    return this.httpClient.post<{ id: number }>(`${globals.apiBaseUrl}/users/user/get_id/`, { uid }, { headers }).pipe(
      map((response) => response.id)
    );
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
    if (!isPlatformBrowser(this.platformId)) return of('');

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
    this.csrfToken = token;
  }
}