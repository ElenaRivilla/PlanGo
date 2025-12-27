import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { Message } from './message';

@Injectable({
  providedIn: 'root',
})
export class MessageService {
  private messageSource = new Subject<Message | Message[]>();
  private clearSource = new Subject<string>();

  messageObserver: Observable<Message | Message[]> = this.messageSource.asObservable();
  clearObserver: Observable<string> = this.clearSource.asObservable();

  add(message: Message): void {
    this.messageSource.next(message);
  }

  addAll(messages: Message[]): void {
    this.messageSource.next(messages);
  }

  clear(key?: string): void {
    this.clearSource.next(key || '');
  }
}