import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Observable } from 'rxjs';
import {globals} from '../globals';

@Injectable({ providedIn: 'root' })
export class ExpensesService {
  //private apiUrl = `${globals.apiBaseUrl}/expenses/expense/user/`;

  constructor( 
    private httpClient: HttpClient, 
    @Inject(PLATFORM_ID) private platformId: Object) {}

  private createHeaders(): HttpHeaders {

    let token = '';
    if (isPlatformBrowser(this.platformId)) {
      token = localStorage.getItem(globals.keys.accessToken) || '';
    }
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
  }

  getExpensesByLoggedUser(): Observable<any> {
    const headers = this.createHeaders();
    return this.httpClient.get(`${globals.apiBaseUrl}/expenses/expense/user/`, { headers });
  }

  getExpenseDetail(expense_id: number): Observable<any> {
    const headers = this.createHeaders();
    return this.httpClient.get(`${globals.apiBaseUrl}/expenses/expense/${expense_id}/`, { headers });
  }

  createExpense(expense: any): Observable<any> {
    const headers = this.createHeaders();
    return this.httpClient.post(`${globals.apiBaseUrl}/expenses/create_expense/`, expense, { headers });
  }
  
}