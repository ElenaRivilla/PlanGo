import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map, Observable, switchMap, throwError } from 'rxjs';
import { globals } from '../globals';
import { MessageService } from '../messageService';

@Injectable({
  providedIn: 'root'
})
export class SearchPlacesService {

  categoriaSeleccionada: string | null = null;

  private csrfToken: string = '';

  constructor(
    public httpClient: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object,
    public toast: MessageService
  ) {
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

  googlePlacesSearchNearby(payload: { latitude: number, longitude: number, radius?: number }): Observable<any> {
    let headers = this.createHeaders();
    return this.httpClient.post(`${globals.apiBaseUrl}/places/google_places_search_nearby/`, payload, { headers });
  }

  saveAccommodationWithImages(payload: any): Observable<any> {
    let headers = this.createHeaders();
    return this.httpClient.post(`${globals.apiBaseUrl}/places/create_accommodation/`, payload, { headers });
  }

  saveRestaurantWithImages(payload: any): Observable<any> {
    let headers = this.createHeaders();
    return this.httpClient.post(`${globals.apiBaseUrl}/places/create_restaurant/`, payload, { headers });
  }

  saveActivityWithImages(payload: any): Observable<any> {
    let headers = this.createHeaders();
    return this.httpClient.post(`${globals.apiBaseUrl}/places/create_activity/`, payload, { headers });
  }

}