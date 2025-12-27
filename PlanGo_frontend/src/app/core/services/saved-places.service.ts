import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { map, Observable, throwError } from 'rxjs';
import { globals } from '../globals';

@Injectable({
    providedIn: 'root'
})
export class SavedPlacesService {
    private csrfToken: string = '';

    constructor(
        private httpClient: HttpClient,
        @Inject(PLATFORM_ID) private platformId: Object
    ) { }

    getSavedPlacesByCategory(userId: number): Observable<any> {
        let token = '';
        let headers = this.createHeaders();
        if (isPlatformBrowser(this.platformId)) {
            token = localStorage.getItem(globals.keys.accessToken) || '';
        }
        return this.httpClient.get(`${globals.apiBaseUrl}/places/saved_places/by_category/${userId}/`, { headers });
    }

    saveSavedPlaces(payload: any): Observable<any> {
        let headers = this.createHeaders();
        return this.httpClient.post(`${globals.apiBaseUrl}/places/create_saved_place/`, payload, { headers, withCredentials: true });
    }


    private createHeaders(): HttpHeaders {
        let token = '';
        let csrfToken = '';
        if (isPlatformBrowser(this.platformId)) {
            token = localStorage.getItem(globals.keys.accessToken) || '';
            const match = document.cookie.match(/csrftoken=([^;]+)/);
            csrfToken = match ? match[1] : '';
        }

        return new HttpHeaders({
            Authorization: `Bearer ${token}`,
            'X-CSRFToken': csrfToken,
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