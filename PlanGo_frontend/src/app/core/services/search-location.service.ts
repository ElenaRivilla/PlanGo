import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map, Observable, switchMap, throwError, of } from 'rxjs';
import { globals } from '../globals';
import { MessageService } from '../messageService';

@Injectable({
    providedIn: 'root'
})
export class SearchLocationService {
    activePhotoIndex: number = 0;
    selectedPlaceImages: any[] = [];
    activeMarker: any = null;

    private csrfToken: string = '';

    constructor(
        public httpClient: HttpClient,
        @Inject(PLATFORM_ID) private platformId: Object,
        public toast: MessageService
    ) {
    }

    private createHeaders(): HttpHeaders {
        let token = '';
        let csrfToken = '';
        if (isPlatformBrowser(this.platformId)) {
            try {
                token = localStorage.getItem(globals.keys.accessToken) || '';
                // Lee la cookie csrftoken directamente
                const match = typeof document !== 'undefined' ? document.cookie.match(/csrftoken=([^;]+)/) : null;
                csrfToken = match ? match[1] : '';
            } catch (e) {
                token = '';
                csrfToken = '';
            }
        }

        return new HttpHeaders({
            Authorization: `Bearer ${token}`,
            'X-CSRFToken': csrfToken,
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
        this.csrfToken = token.replace(/^"|"$/g, '');
    }

    getAllCategories(destinationId: any): Observable<any> {
        let headers = this.createHeaders();
        return this.httpClient.post(
            `${globals.apiBaseUrl}/places/get_categories/`, { destination_id: destinationId }, { headers, withCredentials: true }
        );
    }

}