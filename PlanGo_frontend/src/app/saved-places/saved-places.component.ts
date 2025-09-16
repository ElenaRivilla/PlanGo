import { Component, Input, ViewChild, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { MapComponent } from '../map/map.component';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../header/header.component';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ParticipantsComponent } from '../participants/participants.component';
import { FormsModule } from '@angular/forms';
import { Destination } from '../destinations/interfaces/destinations.interface';
import { BaseToastService } from '../core/services/base-toast.service';
import { BackButtonComponent } from '../core/back-button/back-button.component';
import { SearchLocationService } from '../core/services/search-location.service';
import { ApiKeyService } from '../core/services/api-key.service';
import { SavedPlacesService } from '../core/services/saved-places.service';
import { ItinerariesService } from '../core/services/itineraries.service';

@Component({
  selector: 'app-saved-places',
  standalone: true,
  imports: [
    CommonModule,
    HeaderComponent,
    MapComponent,
    ParticipantsComponent,
    FormsModule,
    BackButtonComponent,
  ],
  templateUrl: './saved-places.component.html',
  styleUrl: './saved-places.component.css',
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class SavedPlacesComponent {
  @ViewChild('participants') participantsComponent!: ParticipantsComponent;
  @ViewChild('mapRef') mapComponent!: MapComponent;
  userId: number = 0;
  selectedSection: string = '';
  currentDestination!: Destination;
  selectedDestination: Destination[] = [];
  accommodations: any[] = [];
  restaurants: any[] = [];
  activities: any[] = [];
  svgIcons: SafeHtml[] = [];
  errorMessage: string = '';
  activePhotoIndex: number = 0;
  selectedPlaceImages: any[] = [];
  googlePlacesApiKey?: string;
  markers: { lat: number, lng: number, label?: string, place?: any }[] = [];
  selectedPlace: any = null;
  mapLocation: any = { lat: 39.720007, lng: 2.910419 }; // o el centro por defecto

  sections = [
    { title: 'Alojamientos', isOpen: false },
    { title: 'Comer y beber', isOpen: false },
    { title: 'Cosas que hacer', isOpen: false },
  ];
  constructor(
    private sanitizer: DomSanitizer,
    private searchLocationService: SearchLocationService,
    private itinerariesService: ItinerariesService,
    private toast: BaseToastService,
    private apiKeyService: ApiKeyService,
    private savedPlacesService: SavedPlacesService,
  ) {

    const rawIcons = [
      `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="white" class="h-8 w-8">
        <path d="M3 5V19M3 16H21M21 19V13.2C21 12.0799 21 11.5198 20.782 11.092C20.5903 10.7157 20.2843 10.4097 19.908 10.218C19.4802 10 18.9201 10 17.8 10H11V15.7273M7 12H7.01M8 12C8 12.5523 7.55228 13 7 13C6.44772 13 6 12.5523 6 12C6 11.4477 6.44772 11 7 11C7.55228 11 8 11.4477 8 12Z" />
      </svg>`,
      `<svg fill="#ffffff" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" class="h-8 w-8">
        <path d="M16.84,11.63A3,3,0,0,0,19,10.75l2.83-2.83a1,1,0,0,0,0-1.41,1,1,0,0,0-1.42,0L17.55,9.33a1,1,0,0,1-1.42,0h0L19.67,5.8a1,1,0,1,0-1.42-1.42L14.72,7.92a1,1,0,0,1,0-1.41l2.83-2.83a1,1,0,1,0-1.42-1.42L13.3,5.09a3,3,0,0,0,0,4.24h0L12,10.62,3.73,2.32l-.1-.06a.71.71,0,0,0-.17-.11l-.18-.07L3.16,2H3.09l-.2,0a.57.57,0,0,0-.18,0,.7.7,0,0,0-.17.09l-.16.1-.07,0-.06.1a1,1,0,0,0-.11.17,1.07,1.07,0,0,0-.07.19s0,.07,0,.11a11,11,0,0,0,3.11,9.34l2.64,2.63-5.41,5.4a1,1,0,0,0,0,1.42,1,1,0,0,0,.71.29,1,1,0,0,0,.71-.29L9.9,15.57h0l2.83-2.83h0l2-2A3,3,0,0,0,16.84,11.63ZM9.19,13.45,6.56,10.81A9.06,9.06,0,0,1,4,5.4L10.61,12Zm6.24.57A1,1,0,0,0,14,15.44l6.3,6.3A1,1,0,0,0,21,22a1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.42Z" />
      </svg>`,
      `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="white" class="h-8 w-8">
        <path stroke-linecap="round" stroke-linejoin="round" d="M14.25 6.087c0-.355.186-.676.401-.959.221-.29.349-.634.349-1.003 0-1.036-1.007-1.875-2.25-1.875s-2.25.84-2.25 1.875c0 .369.128.713.349 1.003.215.283.401.604.401.959v0a.64.64 0 0 1-.657.643 48.39 48.39 0 0 1-4.163-.3c.186 1.613.293 3.25.315 4.907a.656.656 0 0 1-.658.663v0c-.355 0-.676-.186-.959-.401a1.647 1.647 0 0 0-1.003-.349c-1.036 0-1.875 1.007-1.875 2.25s.84 2.25 1.875 2.25c.369 0 .713-.128 1.003-.349.283-.215.604-.401.959-.401v0c.31 0 .555.26.532.57a48.039 48.039 0 0 1-.642 5.056c1.518.19 3.058.309 4.616.354a.64.64 0 0 0 .657-.643v0c0-.355-.186-.676-.401-.959a1.647 1.647 0 0 1-.349-1.003c0-1.035 1.008-1.875 2.25-1.875 1.243 0 2.25.84 2.25 1.875 0 .369-.128.713-.349 1.003-.215.283-.4.604-.4.959v0c0 .333.277.599.61.58a48.1 48.1 0 0 0 5.427-.63 48.05 48.05 0 0 0 .582-4.717.532.532 0 0 0-.533-.57v0c-.355 0-.676.186-.959.401-.29.221-.634.349-1.003.349-1.035 0-1.875-1.007-1.875-2.25s.84-2.25 1.875-2.25c.37 0 .713.128 1.003.349.283.215.604.401.96.401v0a.656.656 0 0 0 .658-.663 48.422 48.422 0 0 0-.37-5.36c-1.886.342-3.81.574-5.766.689a.578.578 0 0 1-.61-.58v0Z" />
      </svg>`
    ];
    this.svgIcons = rawIcons.map(icon => this.sanitizer.bypassSecurityTrustHtml(icon));
  }

  toggleSection(index: number): void {
    this.sections.forEach((section, i) => {
      section.isOpen = i === index ? !section.isOpen : false;
    });

    if (this.sections[index].isOpen) {
      this.selectedSection = this.sections[index].title;
      this.searchLocationService.getAllCategories(this.currentDestination.destination_id).subscribe({
        next: (data: any) => {
          this.accommodations = (data.accommodations || []).map((acc: any) => ({ ...acc, activePhotoIndex: 0 }));
          this.restaurants = (data.restaurants || []).map((rest: any) => ({ ...rest, activePhotoIndex: 0 }));
          this.activities = (data.activities || []).map((act: any) => ({ ...act, activePhotoIndex: 0 }));
        },
        error: (err: any) => {
          this.errorMessage = 'Error al encontrar las categorias';
          console.error(err);
        }
      });
    } else {
      this.selectedSection = '';
    }
  }

  ngOnInit(): void {
    this.apiKeyService.getGooglePlacesApiKey().subscribe({
      next: (data: any) => {
        this.googlePlacesApiKey = data.googlePlacesApiKey;
      },
      error: (err: any) => {
        console.log("No ha recibido la KEY de Google Places API.")
      }
    });

    this.itinerariesService.getIdUser().subscribe({
      next: (userId: number | null) => {
        if (userId === null) {
          this.toast.showErrorToast('Error al obtener la información del usuario', false);
          this.userId = 0;
          return;
        }
        this.userId = userId;
        this.loadSavedPlaces();
      },
      error: (err: any) => {
        console.error('No se pudo obtener el userId', err);
      }
    });
  }

  loadSavedPlaces() {
    this.savedPlacesService.getSavedPlacesByCategory(this.userId).subscribe({
      next: (data) => {
        this.accommodations = (data.accommodations || []).map((acc: any) => ({
          ...acc.saved_place,
          images: acc.images,
          activePhotoIndex: 0
        }));
        this.restaurants = (data.restaurants || []).map((rest: any) => ({
          ...rest.saved_place,
          images: rest.images,
          activePhotoIndex: 0
        }));
        this.activities = (data.activities || []).map((act: any) => ({
          ...act.saved_place,
          images: act.images,
          activePhotoIndex: 0
        }));
      },
      error: (err) => {
        this.toast.showErrorToastWithoutComplete('No se pudieron cargar los lugares guardados', false)
      }
    });
  }

  onDestinationSelect(destination: Destination): void {
    this.selectedDestination = [destination];
    this.mapLocation = {
      lat: Number(destination.latitude),
      lng: Number(destination.longitude),
    }
  }

  onPlaceSelect(place: any) {
    this.selectedPlace = place;
    this.selectedPlaceImages = place.images || place.photos || [];
    if (place.latitude && place.longitude) {
      const marker = {
        lat: Number(place.latitude),
        lng: Number(place.longitude),
        label: place.accommodation || place.restaurant || place.activity || place.displayName?.text || '',
        place: { ...place },
      };
      this.markers = [marker];
      this.mapLocation = { lat: marker.lat, lng: marker.lng };
      setTimeout(() => {
        const index = this.markers.findIndex(m => m.lat === marker.lat && m.lng === marker.lng);
        if (this.mapComponent && this.mapComponent.openInfoWindow) {
          this.mapComponent.openInfoWindow(index, marker);
        }
      });
    }
  }

  getPhotoUrl(photo: any): string {
    let cleanPhoto = photo.replace(/^"+|"+$/g, '');
    return `https://places.googleapis.com/v1/${cleanPhoto}/media?maxHeightPx=400&key=${this.googlePlacesApiKey}`;
  }
}
