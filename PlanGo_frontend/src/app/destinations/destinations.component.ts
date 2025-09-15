import { Component, CUSTOM_ELEMENTS_SCHEMA, OnInit } from '@angular/core';
import { DestinationService } from '../core/services/destinations.service';
import { ParticipantsComponent } from '../participants/participants.component';
import { Destination } from './interfaces/destinations.interface';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HeaderComponent } from '../header/header.component';
import { GoogleMapsModule } from '@angular/google-maps';
import { MapComponent } from '../map/map.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { CounterDatesComponent } from '../counter-dates/counter-dates.component';
import { ItinerariesService } from '../core/services/itineraries.service';
import { forkJoin, map, Observable, filter, distinctUntilChanged } from 'rxjs';
import { globals } from '../core/globals';
import { ValidatorMessages } from '../core/validators/validator-messages';
import { BaseToastService } from '../core/services/base-toast.service';
import { ToastModule } from 'primeng/toast';
import { BackButtonComponent } from '../core/back-button/back-button.component';

@Component({
  standalone: true,
  selector: 'app-destinations',
  templateUrl: './destinations.component.html',
  styleUrl: './destinations.component.css',
  imports: [
    CommonModule,
    FormsModule,
    HeaderComponent,
    ParticipantsComponent,
    GoogleMapsModule,
    MapComponent,
    NgSelectModule,
    CounterDatesComponent,
    ToastModule,
    BackButtonComponent,
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],

})
export class DestinationsComponent implements OnInit {
  destinations: Destination[] = [];
  selectedItinerary: any = null;
  errorMaxDaysId: number | null = null;
  errorMessage: string = '';
  errorMessageMaxD: string = '';
  selectedItineraryId: number | null = null;
  summary: { [key: number]: any } = {};
  countries: any[] = [];
  allCountries: { code: string, nameEs: string, nameEn: string }[] = [];
  searchText: string = '';
  cities: any[] = [];
  itineraryStartDate!: string;
  itineraryEndDate!: string;
  itineraryTotalDays!: number;
  showMaxDaysError = false;
  ValidatorMessages = ValidatorMessages;
  private maxDaysErrorTimeout: any = null;

  constructor(
    private destinationService: DestinationService,
    private route: ActivatedRoute,
    private router: Router,
    private itineraryService: ItinerariesService,
    private toast: BaseToastService,
  ) { }

  async ngOnInit() { // La idea es que al pulsar un itinerario, recibe su id y muestra destino / destinos
    await this.getCountries();
    this.itineraryStartDate = history.state.itineraryStartDate;
    this.itineraryEndDate = history.state.itineraryEndDate;
    this.itineraryTotalDays = this.calculateTotalDays(this.itineraryStartDate, this.itineraryEndDate);

    this.route.paramMap.pipe(
      map((params): number => Number(params.get('itineraryId'))),
      filter((itineraryId: number) => !!itineraryId),
      distinctUntilChanged()
    ).subscribe((itineraryId: number) => {
      this.fetchItineraryDetails(itineraryId);
      this.fetchDestinationsByItinerary(itineraryId);
      this.fetchCountriesByItinerary(itineraryId);
      this.selectedItineraryId = itineraryId;
    });
  }

  fetchItineraryDetails(itineraryId: number): void {
    if (this.selectedItineraryId === itineraryId) return;

    this.selectedItineraryId = itineraryId; // Actualiza el ID seleccionado
    this.itineraryService.getItineraryById(itineraryId).subscribe({
      next: (itinerary: any) => {
        this.selectedItinerary = itinerary;
      },
      error: (err: any) => {
        console.error('Error fetching itinerary:', err);
        this.selectedItinerary = null;
      }
    });
  }

  calculateTotalDays(start: string, end: string): number {
    let startDate = new Date(start);
    let endDate = new Date(end);
    return Math.max(1, Math.floor((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24)) + 1);
  }


  guardarFechas(event: { idDestino: number; fechaInicio: string; fechaFin: string }): void {
    this.destinationService.updateDateDestination(event.idDestino, {
      start_date: event.fechaInicio,
      end_date: event.fechaFin
    }).subscribe({
      next: () => {
        // Vuelve a cargar los destinos para actualizar los días ocupados
        if (this.selectedItineraryId) {
          this.fetchDestinationsByItinerary(this.selectedItineraryId);
        }
      },
      error: (err) => {
        this.toast.showErrorToast('Error al actualizar las fechas del destino', false);
      }
    });
  }

  fetchDestinationsByItinerary(itineraryId: number): void {
    this.destinationService.getDestinationsByItinerary(itineraryId).subscribe({
      next: (data: any) => {
        this.destinations = data['User destinations'] || [];
        this.destinations.forEach(dest => {
          this.fetchDestinationSummary(dest.destination_id);
        });
      },
      error: (err: any) => {
        console.error(err);
      }
    });
  }

  fetchCountriesByItinerary(itineraryId: number): void {
    this.destinationService.getCountriesByItinerary(itineraryId).subscribe({
      next: (data: any) => {
        this.countries = data.countries;
      },
      error: () => {
        this.countries = [];
      }
    });
  }

  getTotalExpenses(): number {
    return this.destinations.reduce((sum, dest) => {
      let resumen = this.summary[dest.destination_id];
      return sum + (resumen ? resumen.total_expenses || 0 : 0);
    }, 0);
  }

  fetchDestinationSummary(destinationId: number): void {
    this.destinationService.getDestinationSummary(destinationId).subscribe({
      next: (data: any) => {
        this.summary[destinationId] = data;
      },
      error: (err: any) => {
        this.summary[destinationId] = null;
        console.error('No se pudo cargar el resumen del destino', err);
      }
    });
  }

  fetchCountriesByDestination(destinationId: number): void {
    this.destinationService.getCountriesByDestination(destinationId).subscribe({
      next: (data: any) => {
        this.countries = data.countries;
      },
      error: () => {
        this.countries = [];
      }
    });
  }

  async getCountries(): Promise<void> {
    try {
      let response = await fetch(globals.countriesRest)
      let data = await response.json();
      this.allCountries = data
        .map((country: any) => ({
          code: country.cca2,
          nameEs: country.translations?.spa?.common || country.name.common,
          nameEn: country.name.common,
        }))
        .sort((a: any, b: any) => a.nameEs.localeCompare(b.nameEs));
    } catch (error) {
      console.error('Error al obtener los países:', error);
    }
  }

  getCountryCodesByNames(names: string[]): string[] {
    if (!this.allCountries || this.allCountries.length === 0) {
      console.warn('allCountries está vacío o no inicializado.');
      return [];
    }

    if (!names || names.length === 0) {
      console.warn('El arreglo de nombres está vacío o no definido:', names);
      return [];
    }

    // Normaliza los nombres a buscar
    let normalizedNames = names.map(n => n.trim().toLowerCase());

    // Filtra los países comparando con nombres en español e inglés (exact match primero)
    let exactMatches = this.allCountries
      .filter(c => {
        let nameEs = (c.nameEs || '').trim().toLowerCase();
        let nameEn = (c.nameEn || '').trim().toLowerCase();
        return normalizedNames.some(n => n === nameEs || n === nameEn);
      })
      .map(c => c.code);

    if (exactMatches.length > 0) return exactMatches;

    // Si no hay coincidencias exactas, intentar contains (por si vienen abreviaciones o formatos distintos)
    return this.allCountries
      .filter(c => {
        let nameEs = (c.nameEs || '').trim().toLowerCase();
        let nameEn = (c.nameEn || '').trim().toLowerCase();
        return normalizedNames.some(n => nameEs.includes(n) || nameEn.includes(n));
      })
      .map(c => c.code)
  }

  getCitiesMultipleCountries(input: string, countryCodes: string[]): Observable<any[]> {
    let calls = countryCodes.map(code => this.destinationService.getCitiesFromGoogle(input, code));
    return forkJoin(calls).pipe(
      map(results =>
        results.flatMap(r =>
          r.geonames
            ? r.geonames.map((g: any) => g)
            : []
        )
      )
    );
  }

  onCitySearch() {
    let countryCodes = this.getCountryCodesByNames(this.countries);
    this.cities = [];
    if (this.searchText && countryCodes.length > 0) {
      this.getCitiesMultipleCountries(this.searchText, countryCodes).subscribe({
        next: (results: any[]) => {
          this.cities = results;
        },
        error: (err) => {
          this.cities = [];
        },
      });
    } else {
      this.cities = [];
    }
  }

  formatCountries(): string {
    if (!this.selectedItinerary?.countries) return '';

    let countriesArray = this.selectedItinerary.countries.split(',');
    let length = countriesArray.length;

    if (length === 2) {
      return countriesArray.join(' y ');
    } else if (length > 2) {
      let lastCountry = countriesArray.pop();
      return `${countriesArray.join(', ')} y ${lastCountry}`;
    }
    return this.selectedItinerary.countries;
  }

  goPlaces(destinationId: number): void {
    this.router.navigate(['/search/places', this.selectedItineraryId], {
      queryParams: { destinationId }
    });
  }

  onCitySelect(city: any): void {
    if (!this.selectedItineraryId || !this.countries.length) {
      this.errorMessage = 'Faltan datos para crear el destino';
      return;
    }

    let exists = this.destinations.some(
      dest => dest.city_name.trim().toLowerCase() === city.name.trim().toLowerCase()
    );
    if (exists) {
      this.errorMessage = ValidatorMessages['destinationDuplicate']
      return;
    }

    let country = city.countryName || city.country || this.countries[0];

    let payload: Omit<Destination, 'destination_id'> = {
      itinerary: this.selectedItineraryId,
      country: country,
      city_name: city.toponymName,
      start_date: this.itineraryStartDate as any,
      end_date: this.itineraryEndDate as any,
      latitude: Number(city.lat),
      longitude: Number(city.lng),
    };

    this.destinationService.createDestination(payload).subscribe({
      next: () => {
        this.fetchDestinationsByItinerary(this.selectedItineraryId!);
        this.toast.showSuccessToast('Se ha añadido el destino', false);
        this.cities = [];
        this.errorMessage = '';
      },
      error: (err) => {
        this.errorMessage = 'Error al crear el destino';
        console.error(err);
      }
    });
  }

  reloadDestination(destinationId: number) {
    this.fetchDestinationsByItinerary(this.selectedItineraryId!);
  }

  calculateDays(start: string | Date, end: string | Date): number {
    let startDate = typeof start === 'string' ? new Date(start) : start;
    let endDate = typeof end === 'string' ? new Date(end) : end;
    return Math.max(1, Math.floor((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24)) + 1);
  }

  getOccupiedDays(): number {
    let total = 0;
    for (let dest of this.destinations) {
      if (dest.start_date && dest.end_date) {
        let start = new Date(dest.start_date);
        let end = new Date(dest.end_date);
        // Sumamos +1 para incluir ambos días
        total += Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1;
      }
    }
    return total;
  }

  getOtherOccupiedDays(currentDestinationId: number): number {
    return this.destinations
      .filter(dest => dest.destination_id !== currentDestinationId)
      .reduce((total, dest) => {
        if (dest.start_date && dest.end_date) {
          let start = new Date(dest.start_date);
          let end = new Date(dest.end_date);
          total += Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1;
        }
        return total;
      }, 0);
  }

  onMaxDaysReached(destinationId: number) {
    this.showMaxDaysError = true;
    if (this.maxDaysErrorTimeout) clearTimeout(this.maxDaysErrorTimeout);
    this.maxDaysErrorTimeout = setTimeout(() => {
      this.showMaxDaysError = false;
    }, 2500);
  }

  onInputClick() {
    if (this.getOccupiedDays() >= this.itineraryTotalDays) {
      this.showMaxDaysError = true;
      if (this.maxDaysErrorTimeout) clearTimeout(this.maxDaysErrorTimeout);
      this.maxDaysErrorTimeout = setTimeout(() => {
        this.showMaxDaysError = false;
      }, 3000);
    }
  }
}