import { Component, OnInit, CUSTOM_ELEMENTS_SCHEMA, HostListener } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ItinerariesService } from '../core/services/itineraries.service';
import { Itinerary } from './interfaces/itinerary.interface';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../header/header.component';
import { GoogleMapsModule } from '@angular/google-maps';
import { Router } from '@angular/router';
import { MapComponent } from '../core/map/map.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { switchMap, throwError } from 'rxjs';
import { globals } from '../core/globals';
import { BaseToastService } from '../core/services/base-toast.service';
import { ToastModule } from 'primeng/toast';
import { CalendarModule } from 'primeng/calendar';
import { CustomValidators } from '../core/validators/custom-validators';
import { ValidatorMessages } from '../core/validators/validator-messages';

@Component({
  standalone: true,
  selector: 'app-itineraries',
  templateUrl: './itineraries.component.html',
  styleUrls: ['./itineraries.component.css'],
  imports: [
    CommonModule,
    HeaderComponent,
    GoogleMapsModule,
    MapComponent,
    ReactiveFormsModule,
    NgSelectModule,
    ToastModule,
    CalendarModule],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class ItinerariesComponent implements OnInit {
  itineraries: Itinerary[] = [];
  errorMessage: string = '';
  showForm: boolean = false;
  itineraryForm: FormGroup;
  allCountries: { code: string; name: string }[] = [];
  currentDate: Date = new Date();
  ValidatorMessages = ValidatorMessages;
  formSubmitted = false;

  constructor(
    private itinerariesService: ItinerariesService,
    private router: Router,
    private fb: FormBuilder,
    private toast: BaseToastService
  ) {
    this.itineraryForm = this.fb.group({
      itineraryName: ['', Validators.required],
      countries: [[], Validators.required],
      startDate: [this.currentDate.toISOString().split('T')[0], Validators.required],
      endDate: ['', Validators.required],
    }, {
      validators: CustomValidators.endDateAfterStartDate()
    });
  }

  async ngOnInit(): Promise<void> {
    this.getItineraries();
    await this.getCountries();
  }

  @HostListener('document:keydown.escape', ['$event'])
  onEscKey(event: KeyboardEvent) {
    if (this.showForm) this.toggleForm();
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
    if (!this.showForm) {
      this.itineraryForm.reset({
        itineraryName: '',
        countries: [],
        startDate: this.currentDate.toISOString().split('T')[0],
        endDate: ''
      });
      this.formSubmitted = false;
    }
  }

  private formatDate(date: any): string {
    if (!date) return '';
    if (typeof date === 'string') {
      // Si ya es string, intenta devolver solo la parte YYYY-MM-DD
      return date.split('T')[0];
    }
    if (date instanceof Date) {
      return date.toISOString().split('T')[0];
    }
    return '';
  }

  onSubmit(): void {
    this.formSubmitted = true;
    if (this.itineraryForm.valid) {
      this.itinerariesService.getCsrfTokenFromServer().pipe(
        switchMap((csrfToken) => {
          this.itinerariesService.setCsrfToken(csrfToken);

          return this.itinerariesService.getIdUser().pipe(
            switchMap((userId) => {
              if (userId === null) {
                this.toast.showErrorToast('Error al obtener la información del usuario', false);
                return throwError(() => new Error('User id not available'));
              }

              let countries = this.itineraryForm.get('countries')?.value.map((country: string) => country);
              let newItinerary: Itinerary = {
                itinerary_name: this.itineraryForm.get('itineraryName')?.value,
                creator_user: userId,
                creation_date: new Date().toISOString().split('T')[0],
                start_date: (this.itineraryForm.get('startDate')?.value).toISOString().split('T')[0],
                end_date: (this.itineraryForm.get('endDate')?.value).toISOString().split('T')[0],
                countries: countries,
              };
              this.toast.showSuccessToast('Se han añadido el itinerario', false);
              return this.itinerariesService.createItinerary(newItinerary);
            })
          );
        })
      ).subscribe({
        next: (response) => {
          this.getItineraries();
          this.showForm = false;
          this.itineraryForm.reset({
            itineraryName: '',
            countries: [],
            startDate: this.currentDate.toISOString().split('T')[0],
            endDate: ''
          });
          this.formSubmitted = false;
        },
        error: (err) => {
          console.error('Error al guardar el itinerario:', err);
        },
      });
      this.formSubmitted = false;
    } else {
      this.itineraryForm.markAllAsTouched();
      this.itineraryForm.updateValueAndValidity();
      console.error('Formulario inválido');
    }
  }

  getItineraries(): void {
    this.itinerariesService.getItineraries().subscribe({
      next: (data: { itineraries: Itinerary[] }) => {
        this.itineraries = data.itineraries;
      },
      error: (err: any) => {
        this.errorMessage = 'No se pudieron cargar los itinerarios.';
        console.error('Error al obtener itinerarios:', err);
      }
    });
  }

  async getCountries(): Promise<void> {
    try {
      let response = await fetch(globals.countriesRest);
      let data = await response.json();
      this.allCountries = data
        .map((country: any) => ({
          code: country.cca2,
          name: country.translations?.spa?.common || country.name.common,
        }))
        .sort((a: any, b: any) => a.name.localeCompare(b.name));
    } catch (error) {
      console.error('Error al obtener los países:', error);
    }
  }

  onCountriesChange(): void {
    let selectedCountries = this.itineraryForm.get('destinations')?.value || [];
  }

  goToDestinations(itineraryId: number | undefined): void {
    let itinerary = this.itineraries.find(it => it.itinerary_id === itineraryId);
    if (!itinerary) return;
    this.router.navigate(['/destinations', itineraryId], {
      state: {
        itineraryStartDate: itinerary.start_date,
        itineraryEndDate: itinerary.end_date
      }
    });
  }
}