import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { globals } from '../globals';
import { BaseHttpService } from './base-http.service';
import { MessageService } from '../messageService';
import { user } from '@angular/fire/auth';

@Injectable({
  providedIn: 'root',
})
export class ParticipantsService extends BaseHttpService {
  constructor(
    public override httpClient: HttpClient, 
    @Inject(PLATFORM_ID) private platformId: Object,
    public override toast: MessageService 
  ) {
    super(httpClient, toast); 
  }

  createParticipant(participant: any): Observable<any> {
    const headers = this.createHeaders();
    return this.httpClient.post(`${globals.apiBaseUrl}/users/participant/create/`, participant, { headers });
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

  getParticipantsByDestination(destinationId: number): Observable<any> {
    const headers = this.createHeaders();
    return this.httpClient.get(`${globals.apiBaseUrl}/users/participants/by_destination/${destinationId}`, { headers });
  }
}
