import { CommonModule } from "@angular/common";
import { Component } from "@angular/core";
import { trigger, style, transition, animate, state } from '@angular/animations';
import { HeaderComponent } from "../header/header.component";
import { MapComponent } from '../core/map/map.component';
import { ParticipantsComponent } from "../participants/participants.component";
import { FormsModule } from "@angular/forms";
import { DomSanitizer, SafeHtml } from "@angular/platform-browser";
import { Destination } from "../destinations/interfaces/destinations.interface";
import { ActivatedRoute, ParamMap, Router } from "@angular/router";
import { DestinationService } from "../core/services/destinations.service";
import { BaseToastService } from '../core/services/base-toast.service';
import { SearchPlacesService } from '../core/services/search-places.service';
import { ApiKeyService } from "../core/services/api-key.service";
import { BackButtonComponent } from '../core/back-button/back-button.component';
import { ViewChild } from '@angular/core';
import { ToastModule } from "primeng/toast";
import { ItinerariesService } from "../core/services/itineraries.service";
import { SavedPlacesService } from "../core/services/saved-places.service";

@Component({
  selector: 'app-search-places',
  standalone: true,
  templateUrl: './search-places.component.html',
  styleUrl: './search-places.component.css',
  imports: [
    CommonModule,
    HeaderComponent,
    MapComponent,
    ParticipantsComponent,
    FormsModule,
    BackButtonComponent,
    ToastModule,
  ],
  animations: [
    trigger('accordionContent', [
      transition(':enter', [
        style({ height: 0, opacity: 0, overflow: 'hidden' }),
        animate('300ms cubic-bezier(0.4,0,0.2,1)', style({ height: '*', opacity: 1, overflow: 'hidden' })),
      ]),
      transition(':leave', [
        style({ height: '*', opacity: 1, overflow: 'hidden' }),
        animate('300ms cubic-bezier(0.4,0,0.2,1)', style({ height: 0, opacity: 0, overflow: 'hidden' })),
      ]),
    ]),
    trigger('hoverAnimation', [
      state('default', style({ transform: 'scale(1)' })),
      state('hover', style({ transform: 'scale(1.1)' })),
      transition('default <=> hover', animate('300ms ease-in-out')),
    ]),
  ]
})

export class SearchPlacesComponent {
  @ViewChild('mapRef') mapComponent!: MapComponent;
  selectedCategory: string | null = null;
  currentDestination?: Destination;
  mapLocation: google.maps.LatLngLiteral = { lat: 39.72596642771257, lng: 2.914616467674367 };
  destinations: Destination[] = [];
  svgIcons: SafeHtml[] = [];
  savedPlaceIdsByPlace: string[] = [];
  savedPlaceIdsByPlaces: string[] = [];
  sectionOpen = false;
  places: any[] = [];
  googlePlacesApiKey?: string;
  activeSection: string | null = null;
  selectedPlace: any = null;
  selectedPlaceImages: any[] = [];
  savedPlaceIds: string[] = [];
  savedPlaceIds2: string[] = [];
  markers: { lat: number, lng: number, label?: string, place?: any }[] = [];
  sections = [
    { title: 'Alojamientos', isOpen: false },
    { title: 'Comer y beber', isOpen: false },
    { title: 'Cosas que hacer', isOpen: false },
  ];

  buttonStates: { [key: string]: string } = {};

  constructor(
    private sanitizer: DomSanitizer,
    private destinationService: DestinationService,
    private searchPlacesService: SearchPlacesService,
    private route: ActivatedRoute,
    private router: Router,
    private toast: BaseToastService,
    private apiKeyService: ApiKeyService,
    private itinerariesService: ItinerariesService,
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

  ngOnInit(): void {
    this.route.queryParamMap.subscribe((params: ParamMap) => {
      this.selectedCategory = params.get('category');
      this.activeSection = params.get('category');
      this.sections.forEach(section => section.isOpen = false);
      let destinationIdParam = params.get('destinationId');
      let destinationId = destinationIdParam ? Number(destinationIdParam) : null;
      this.currentDestination = undefined; // Limpia el destino anterior
      if (destinationId) {
        this.destinationService.getDestinations().subscribe({
          next: (data: any) => {
            let destinations: Destination[] = Array.isArray(data) ? data : data.destination || [];
            this.currentDestination = destinations.find(dest => dest.destination_id === destinationId);
            if (this.currentDestination && this.currentDestination.latitude && this.currentDestination.longitude) {
              this.mapLocation = {
                lat: Number(this.currentDestination.latitude),
                lng: Number(this.currentDestination.longitude),
              };
              this.loadPlaces(this.mapLocation.lat, this.mapLocation.lng);
            } else {
              // Si no encuentra el destino, usa el valor por defecto
              this.mapLocation = { lat: 39.72596642771257, lng: 2.914616467674367 };

            }
          },
          error: () => {
            this.currentDestination = undefined;
            this.mapLocation = { lat: 39.72596642771257, lng: 2.914616467674367 };
            this.places = [];
          }
        });
      } else {
        // Si no hay destinationId, usa el valor por defecto
        this.mapLocation = { lat: 39.72596642771257, lng: 2.914616467674367 };
        this.loadPlaces(this.mapLocation.lat, this.mapLocation.lng);
      }
    });
  }

  ngAfterViewInit(): void {
    this.apiKeyService.getGooglePlacesApiKey().subscribe({
      next: (data: any) => {
        this.googlePlacesApiKey = data.googlePlacesApiKey;
      },
      error: (err: any) => {
        console.log("No ha recibido la KEY de Google Places API.")
      }
    });
  }

  toggleSection(index: number): void {
    this.sections.forEach((section, i) => {
      if (i === index) {
        section.isOpen = !section.isOpen;
      } else {
        section.isOpen = false;
      }
    });
  }

  loadPlaces(lat: number, lng: number): void {
    this.itinerariesService.getIdUser().subscribe({
      next: (userId: number | null) => {
        if (userId === null) {
          this.toast.showErrorToast('Error al obtener la información del usuario', false);
          return;
        }
        let payload = {
          latitude: lat,
          longitude: lng,
          radius: 50000,
          category: this.selectedCategory,
          user_id: userId
        };
        this.searchPlacesService.googlePlacesSearchNearby(payload).subscribe({
          next: (data: any) => {
            // Suponiendo que tienes un array this.savedPlaceIds con los IDs guardados
            this.places = (data.places || [])
              .filter((p: any) => p.photos && p.photos.length > 0)
              .map((place: any) => ({
                ...place,
                isSaveByPlace: this.savedPlaceIdsByPlace.includes(place.id),
                isSaveByPlaces: this.savedPlaceIdsByPlaces.includes(place.id)
              }));
          },
          error: (err: any) => {
            this.places = [];
            this.toast.showErrorToast('No se pudieron cargar los lugares', false);
          }
        });
      },
      error: () => {
        this.toast.showErrorToast('No se pudo obtener el usuario', false);
      }
    });
  }

  getPhotoUrl(photo: any): string {
    if (photo?.name && this.googlePlacesApiKey) {
      return `https://places.googleapis.com/v1/${photo.name}/media?maxHeightPx=400&key=${this.googlePlacesApiKey}`;
    }
    return 'assets/no-image.png';
  }

  getActiveSectionIndex(): number {
    return this.sections.findIndex(s => s.title === this.activeSection);
  }

  onPlaceSelect(place: any) {
    this.selectedPlace = place;
    // Guarda el array de imágenes (photos) del lugar seleccionado
    this.selectedPlaceImages = place.photos || [];
    if (place.location && place.location.latitude && place.location.longitude) {
      const marker = {
        lat: Number(place.location.latitude),
        lng: Number(place.location.longitude),
        label: place.displayName?.text || '',
        place: { ...place }
      };
      this.markers = [{
        lat: Number(place.location.latitude),
        lng: Number(place.location.longitude),
        label: place.displayName?.text || '',
        place: { ...place }
      }];
      this.mapLocation = {
        lat: Number(place.location.latitude),
        lng: Number(place.location.longitude)
      };
      setTimeout(() => {
        let index = this.markers.findIndex(m => m.lat === marker.lat && m.lng === marker.lng);
        this.mapComponent.openInfoWindow(index, marker);
      });
    }
  }

  savePlace(place: any) {
    if (this.savedPlaceIds.includes(place.id)) {
      this.toast.showErrorToast('Este lugar ya ha sido guardado', false);
      return;
    }

    this.itinerariesService.getIdUser().subscribe({
      next: (userId: number | null) => {
        if (userId === null) {
          this.toast.showErrorToast('Error al obtener la información del usuario', false);
          return;
        }
        let payload = {
          user_id: userId,
          place_id: place.id,
          destination: this.currentDestination?.destination_id,
          name: place.displayName?.text,
          primary_type: place.primaryType,
          rating: place.rating,
          formattedAddress: place.formattedAddress,
          latitude: place.location?.latitude,
          longitude: place.location?.longitude,
          images: (place.photos || []).map((photo: any) => photo.name),
          isSave: true
        };
        let saveObservable;

        switch (this.selectedCategory) {
          case 'Alojamientos':
            saveObservable = this.searchPlacesService.saveAccommodationWithImages(payload);
            break;
          case 'Comer y beber':
            saveObservable = this.searchPlacesService.saveRestaurantWithImages(payload);
            break;
          case 'Cosas que hacer':
            saveObservable = this.searchPlacesService.saveActivityWithImages(payload);
            break;
          default:
            this.toast.showErrorToast('Tipo de lugar no soportado', false);
            return;
        }

        saveObservable.subscribe({
          next: (res) => {
            this.savedPlaceIds.push(place.id);
            place.isSaveByPlace = true;
            this.toast.showSuccessToast('Lugar guardado correctamente', false);
          },
          error: (err) => {
            this.toast.showErrorToast('Error al guardar el lugar, ya ha sido guardado previamente', false);
          }
        });
      },
      error: (err: any) => {
        this.toast.showErrorToast('No se pudo obtener el usuario', false);
      }
    });
  }

  savePlaces(place: any) {
    if (this.savedPlaceIds2.includes(place.id)) {
      this.toast.showErrorToast('Este lugar ya ha sido guardado', false);
      return;
    }

    this.itinerariesService.getIdUser().subscribe({
      next: (userId: number | null) => {
        if (userId === null) {
          this.toast.showErrorToast('Error al obtener la información del usuario', false);
          return;
        }
        let payload = {
          user_id: userId,
          place_id: place.id,
          destination: this.currentDestination?.destination_id,
          name: place.displayName?.text,
          primary_type: place.primaryType ? place.primaryType : (place.types && place.types.length > 0 ? place.types[0] : ''),
          rating: place.rating,
          formattedAddress: place.formattedAddress,
          latitude: place.location?.latitude,
          longitude: place.location?.longitude,
          images: (place.photos || []).map((photo: any) => photo.name),
          isSave: true
        };

        this.savedPlacesService.saveSavedPlaces(payload).subscribe({
          next: (res: any) => {
            this.savedPlaceIds2.push(place.id);
            place.isSaveByPlaces = true;
            this.toast.showSuccessToast('Lugar guardado correctamente', false);
          },
          error: (err: any) => {
            this.toast.showErrorToast('Error al guardar el lugar, ya ha sido guardado previamente', false);
          }
        });
      },
      error: (err: any) => {
        this.toast.showErrorToast('No se pudo obtener el usuario', false);

      }
    });
  }

  setHoverState(key: string, state: string): void {
    this.buttonStates[key] = state;
  }
}