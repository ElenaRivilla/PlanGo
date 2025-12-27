import { Component, OnInit, HostListener, CUSTOM_ELEMENTS_SCHEMA, ChangeDetectorRef } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray, ReactiveFormsModule } from '@angular/forms';
import { DestinationService } from '../core/services/destinations.service';
import { ItinerariesService } from '../core/services/itineraries.service';
import { ParticipantsService } from '../core/services/participants.service';
import { ValidatorMessages } from '../core/validators/validator-messages';
import { CustomValidators } from '../core/validators/custom-validators';
import { ExpensesService } from '../core/services/expenses.service';
import { UserExpenses } from './interfaces/userExpenses.interface';
import { HeaderComponent } from '../header/header.component';
import { Expenses } from './interfaces/expenses.interface';
import { GoogleMapsModule } from '@angular/google-maps';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { BaseToastService } from '../core/services/base-toast.service';
import { ToastModule } from 'primeng/toast';
import { BackButtonComponent } from '../core/back-button/back-button.component';

@Component({
  standalone: true,
  selector: 'app-expenses',
  templateUrl: './expenses.component.html',
  styleUrl: './expenses.component.css',
  imports: [
    CommonModule,
    HeaderComponent,
    GoogleMapsModule,
    ReactiveFormsModule,
    ToastModule,
    BackButtonComponent
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})

export class ExpensesComponent implements OnInit {
  itineraries: any[] = [];
  destinations: any[] = [];
  selectedItineraryId: number | null = null;
  selectedDestinationId: number | null = null;
  selectedExpense: any = null;
  expenses: Expenses[] = [];
  participants: any[] = [];
  expenseForm: FormGroup;
  showForm: boolean = false;
  formSubmitted: boolean = false;
  errorMessage: string = '';
  validatorMessages = ValidatorMessages;
  center = { lat: 39.720007, lng: 2.910419 };
  zoom = 13;
  map!: google.maps.Map;
  selectedDestination: any = null;
  mapOptions: google.maps.MapOptions = {
    mapId: 'DEMO_MAP_ID',
    disableDefaultUI: true,
  };

  constructor(
    private expensesService: ExpensesService,
    private destinationService: DestinationService,
    private itinerariesService: ItinerariesService,
    private participantsService: ParticipantsService,
    private router: Router,
    private formBuilder: FormBuilder,
    private cdr: ChangeDetectorRef,
    private toast: BaseToastService
  ) {
    this.expenseForm = this.formBuilder.group({
      itinerary: [''],
      destination: [''],
      payer: [''],
      total_amount: [''],
      description: [''],
      date: [''],
      type_expense: ['Personalized', Validators.required],
      debtors: this.formBuilder.array([]),
    }, {
      validators: [
        CustomValidators.itineraryAndDestinationRequired(),
        CustomValidators.payerAndAmountRequired(),
        CustomValidators.debtorsNotExceedTotalAmount(),
        CustomValidators.debtorsAmountRequiredPersonalized(),
        CustomValidators.debtorsSelectRequired(),
      ]
    });
  }

  async ngOnInit(): Promise<void> {
    this.expensesService.getExpensesByLoggedUser().subscribe({
      next: (data) => this.expenses = data.expenses,
      error: (err) => this.errorMessage = 'No se pudieron cargar los gastos.'
    });

    this.destinationService.getDestinations().subscribe({
      next: (data) => this.destinations = data,
      error: (err) => this.errorMessage = 'No se pudieron cargar los destinos.'
    })

    this.itinerariesService.getItineraries().subscribe({
      next: (data: any) => this.itineraries = data.itineraries,
      error: (err: any) => this.itineraries = []
    });

    this.expenseForm.valueChanges.subscribe(() => {
      let { itinerary, destination, payer } = this.expenseForm.value
      if (itinerary && destination && payer) {
        this.formSubmitted = false;
      }
      // Si quieres ocultar todos los mensajes cuando el campo es válido:
      if (this.expenseForm.valid) {
        this.formSubmitted = false;
      }
    });
  }

  @HostListener('document:keydown.escape', ['$event'])
  onEscKey(event: KeyboardEvent) {
    if (this.showForm) this.toggleForm();
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
    this.formSubmitted = false;
    this.errorMessage = '';
    if (this.showForm) {
      this.expenseForm.reset({
        itinerary: '',
        destination: '',
        payer: '',
        total_amount: '',
        description: '',
        type_expense: 'Personalized',
        debtors: [],
      });
    }
  }

  onSubmit(): void {
    this.formSubmitted = true;
    if (this.expenseForm.valid) {
      let formValue = this.expenseForm.value;

      let payerId = Number(formValue.payer);
      let payer = this.participants.find(p => p.participant_id === payerId);

      // Pagador: si es -1 es el usuario, si no es participante invitado
      let paid_by_user = payer?.participant_id === -1 ? payer.user : null;
      let paid_by_name = payer?.participant_id === -1 ? null : payer.participant_name;

      // Deudores: solo el usuario autenticado lleva user, los demás llevan user_name
      let debtors = formValue.debtors.map((debtor: any) => {
        let participant = this.participants.find(p => p.participant_id === Number(debtor.id));
        return {
          participant_id: Number(debtor.id),
          user: participant?.participant_id === -1 ? participant.user : null,
          user_name: participant?.participant_id === -1 ? null : participant?.participant_name,
          amount: debtor.amount
        };
      });

      let newExpense = {
        itinerary: formValue.itinerary,
        destination: formValue.destination,
        paid_by_user,
        paid_by_name,
        total_amount: formValue.total_amount,
        description: formValue.description,
        date: formValue.date,
        type_expense: formValue.type_expense,
        debtors
      };

      this.expensesService.createExpense(newExpense).subscribe({
        next: () => {
          this.expensesService.getExpensesByLoggedUser().subscribe({
            next: (data) => this.expenses = data.expenses
          });
          this.getTotalExpenses();
          let debtorsArray = this.expenseForm.get('debtors') as FormArray;

          while (debtorsArray.length) {
            debtorsArray.removeAt(0);
          }

          this.showForm = false;
          this.toast.showSuccessToast('Se han añadido el gasto', false);
        },
        error: (err) => {
          console.error('Error al guardar el gasto:', err);
        },
      });
    } else {
      console.error("Formulario inválido", this.expenseForm.errors, this.expenseForm.value);
      this.expenseForm.markAllAsTouched();
    }
  }

  goToDestinations(itineraryId: number): void {
    this.router.navigate(['/destinations', itineraryId]);
  }

  getTotalExpenses(): number {
    return this.expenses.reduce((sum, expense) => sum + parseFloat(expense.total_amount as any || '0'), 0)
  }

  getSelectedDestination(destinationId: Expenses): void {
    this.selectedDestination = this.destinations.find(dest => dest.destination_id === destinationId);
  }

  onItineraryChange(): void {
    let itineraryId = this.expenseForm.value.itinerary;
    if (itineraryId) {
      this.destinationService.getDestinationsByItinerary(itineraryId).subscribe({
        next: (data: any) => {
          this.destinations = Array.isArray(data) ? data : data['User destinations'] || [];
        },
        error: (err: any) => this.destinations = []
      });
    } else {
      this.destinations = [];
    }
    this.selectedDestinationId = null;
  }

  onDestinationsChange(): void {

    let destinationId = this.expenseForm.value.destination;
    if (destinationId) {
      this.selectedDestinationId = destinationId;
      this.loadParticipants(destinationId);
    } else {
      this.selectedDestinationId = null;
      this.participants = [];
    }
  }

  onPayerChange(): void {
    let debtorsArray = this.expenseForm.get('debtors') as FormArray;
    debtorsArray.clear();
    this.expenseForm.updateValueAndValidity();
  }

  onClickExpense(expense: any): void {
    this.expensesService.getExpenseDetail(expense.expense_id).subscribe({
      next: (data) => this.selectedExpense = data,
      error: (err) => this.selectedExpense = null
    });
  }

  loadParticipants(destinationId: number): void {
    this.participantsService.getParticipantsByDestination(destinationId).subscribe({
      next: (data: any) => {
        let participants = Array.isArray(data.Participants) ? data.Participants : [];
        // Asigna participant_id = -1 al usuario autenticado si es null
        this.participants = participants.map((p: any) =>
          p.participant_id === null ? { ...p, participant_id: -1 } : p
        );
      },
      error: () => this.participants = [],
    });
  }

  get debtorsControls() {
    return (this.expenseForm.get('debtors') as FormArray).controls;
  }

  get possibleDebtors() {
    let payerId = this.expenseForm?.value?.payer;
    return this.participants.filter(p => (p.user || p.participant_id) !== payerId);
  }

  get userExpenses() {
    return this.expenseForm.get('userExpenses') as FormArray;
  }

  setEqualitarian() {
    this.expenseForm.get('type_expense')?.setValue('Equalitarian');
    let debtorsArray = this.expenseForm.get('debtors') as FormArray;
    debtorsArray.controls.forEach(ctrl => {
      ctrl.get('amount')?.clearValidators();
      ctrl.get('amount')?.setErrors(null);
      ctrl.get('amount')?.disable();
      ctrl.get('amount')?.updateValueAndValidity({ onlySelf: true, emitEvent: false });
    });
    this.cdr.detectChanges();
  }

  setPersonalized() {
    this.expenseForm.get('type_expense')?.setValue('Personalized');
    let debtorsArray = this.expenseForm.get('debtors') as FormArray;
    debtorsArray.controls.forEach(ctrl => {
      ctrl.get('amount')?.setValidators(Validators.required);
      ctrl.get('amount')?.enable();
      ctrl.get('amount')?.updateValueAndValidity({ onlySelf: true, emitEvent: false });
    });
    this.cdr.detectChanges();
  }

  addDebtor(): void {
    //this.formSubmitted = true; // Marca como enviado para mostrar errores
    this.expenseForm.updateValueAndValidity(); // Fuerza la validación de grupo

    // Si existe el error, no añadas el deudor
    if (!this.expenseForm.value.payer) {
      this.formSubmitted = true;
      return;
    }

    let debtorsArray = this.expenseForm.get('debtors') as FormArray;
    let isEqualitarian = this.expenseForm.get('type_expense')?.value === 'Equalitarian';
    let group = this.formBuilder.group({
      id: [null, Validators.required],
      amount: ['', isEqualitarian ? [] : Validators.required]
    });
    if (isEqualitarian) {
      group.get('amount')?.disable();
      group.get('amount')?.updateValueAndValidity({ onlySelf: true, emitEvent: false });
    }
    debtorsArray.push(group);
  }

  removeDebtor(index: number): void {
    let debtorsArray = this.expenseForm.get('debtors') as FormArray;
    debtorsArray.removeAt(index);
  }

  getPossibleDebtors(i: number): any[] {
    let payerParticipantId = String(this.expenseForm.get('payer')?.value);
    let debtorsArray = this.expenseForm.get('debtors') as FormArray;
    let selectedIds = debtorsArray.controls
      .map((ctrl, idx) => idx !== i ? String(ctrl.value.id) : null)
      .filter(id => id !== null);
    return this.participants.filter(p => {
      let id = String(p.participant_id);
      return id !== payerParticipantId && !selectedIds.includes(id);
    });
  }

  addUserExpense(): void {
    this.userExpenses.push(
      this.formBuilder.group({
        user: [''],
        userName: [''],
        amountPaid: [''],
        expectedShare: [''],
        debt: [''],
      })
    );
  }

  removeUserExpense(index: number): void {
    this.userExpenses.removeAt(index);
  }

  isAddDebtorDisabled(): boolean {
    return (
      !this.expenseForm.value.payer || this.possibleDebtors.length === 0 ||
      this.debtorsControls.length >= this.possibleDebtors.length - 1 ||
      this.debtorsControls.some(d => !d.value.id)
    );
  }
}