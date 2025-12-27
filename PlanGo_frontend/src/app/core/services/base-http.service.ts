import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { catchError, Observable, retry, throwError } from 'rxjs';
import { MessageService } from '../messageService';

@Injectable({
  providedIn: 'root'
})
export class BaseHttpService {
  
  private readonly defaultRetryTimes = 0;

  constructor(
    public httpClient: HttpClient,
    public toast: MessageService,
  ) { }
  
  public get<T>(
    url: string,
    headers?: HttpHeaders,
    params?: HttpParams,
    retryTimes: number = this.defaultRetryTimes
  ): Observable<T> {
    return this.httpClient
      .get<T>(url, { headers: headers, params: params })
      .pipe(
        retry(retryTimes), // Retry a failed request up to #retryTimes times
        catchError((error) => this.handleError(error))
      );
  }

  public post<T>(
    url: string,
    body: any,
    headers?: HttpHeaders,
    params?: HttpParams,
    retryTimes: number = this.defaultRetryTimes
  ): Observable<T> {
    return this.httpClient
      .post<T>(url, body, { headers: headers, params: params })
      .pipe(
        retry(retryTimes), // Retry a failed request up to #retryTimes times
        catchError((error) => this.handleError(error))
      );
  }

  public put<T>(
    url: string,
    body: any,
    headers?: HttpHeaders,
    params?: HttpParams,
    retryTimes: number = this.defaultRetryTimes
  ): Observable<T> {
    return this.httpClient
      .put<T>(url, body, { headers: headers, params: params })
      .pipe(
        retry(retryTimes), // Retry a failed request up to #retryTimes times
        catchError((error) => this.handleError(error))
      );
  }

  public delete<T>(
    url: string,
    headers?: HttpHeaders,
    params?: HttpParams,
    retryTimes: number = this.defaultRetryTimes
  ): Observable<T> {
    return this.httpClient
      .delete<T>(url, { headers: headers, params: params })
      .pipe(
        retry(retryTimes), // Retry a failed request up to #retryTimes times
        catchError((error) => this.handleError(error))
      );
  }

  public deleteWithBody<T>(
    url: string,
    headers?: HttpHeaders,
    params?: HttpParams,
    body?: any, 
    retryTimes: number = this.defaultRetryTimes
  ): Observable<T> {
    return this.httpClient
      .request<T>('DELETE', url, { body: body, headers: headers, params: params }) 
      .pipe(
        retry(retryTimes),
        catchError((error) => this.handleError(error))
      );
  }

  public patch<T>(
    url: string,
    body: any,
    headers?: HttpHeaders,
    params?: HttpParams,
    retryTimes: number = this.defaultRetryTimes
  ): Observable<T> {
    return this.httpClient
      .patch<T>(url, body, { headers: headers, params: params })
      .pipe(
        retry(retryTimes), // Retry a failed request up to #retryTimes times
        catchError((error) => this.handleError(error))
      );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error.ErrorCode) {
      // A client-side or network error occurred.
      this.toast.add(
        {
          severity: "error",
          detail: `Error ${ error.error.ErrorCode }`,
          summary: `${ error.error.ErrorMessage }`,
          life: 5000
        });
    } 

    return throwError(() => error);
  }
}