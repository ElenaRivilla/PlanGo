import { Injectable } from '@angular/core';
import { MessageService } from 'primeng/api';

@Injectable({
  providedIn: 'root',
})
export class BaseToastService {

  constructor(private messageService: MessageService) {}

  public showErrorToast( summary: string, sticky: boolean = false) {
    this.showToast("error", "", summary, sticky);
  }

  public showSuccessToast(summary: string, sticky: boolean = false) {
    this.showToast("success", "", summary, sticky);
  }

  public showSuccessToastWithoutComplete(summary: string, sticky: boolean = false) {
    this.showToast("success", '', summary, sticky, 'font-ptoast','font-ptoast');
  }

  public showErrorToastWithoutComplete(summary: string, sticky: boolean = false) {
    this.showToast("error", '', summary, sticky, 'font-ptoast','font-ptoast');
  }

  private showToast(severity: string, detail: string, summary: string, sticky: boolean = false, contentStyleClass: string = '', styleClass: string = '') {
    this.messageService.add({
      severity: severity,
      detail: detail,
      summary: summary,
      sticky: sticky,
      contentStyleClass: contentStyleClass,
      styleClass: styleClass,
    });
  }
}