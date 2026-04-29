import {
  Component, Input, OnInit, AfterViewInit, OnChanges, OnDestroy,
  SimpleChanges, ViewChild, ElementRef, Inject, PLATFORM_ID
} from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { CommonModule } from '@angular/common';
import { ApiKeyService } from '../services/api-key.service';
import { TooltipModule } from 'primeng/tooltip';

@Component({
  standalone: true,
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css'],
  imports: [CommonModule, TooltipModule],
})
export class MapComponent implements OnInit, AfterViewInit, OnChanges, OnDestroy {
  @ViewChild('mapContainer', { static: true }) mapContainer!: ElementRef;
  @Input() center = { lat: 39.720007, lng: 2.910419 };
  @Input() zoom = 13;
  @Input() mapOptions: any = {};
  @Input() markers: { lat: number, lng: number, label?: string, place?: any }[] = [];
  @Input() selectedPlace: any = null;

  activeMarker: any = null;
  activePhotoIndex = 0;
  selectedPlaceImages: any[] = [];
  googlePlacesApiKey?: string;
  showPopup = false;

  private map: any = null;
  private leafletMarkers: any[] = [];
  private L: any = null;
  private resizeObserver?: ResizeObserver;

  constructor(
    public apiKeyService: ApiKeyService,
    @Inject(PLATFORM_ID) private platformId: Object,
  ) {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    if (!isPlatformBrowser(this.platformId)) return;
    this.initMap();
    this.apiKeyService.getGooglePlacesApiKey().subscribe({
      next: (data: any) => { this.googlePlacesApiKey = data.googlePlacesApiKey; },
      error: () => {},
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (!this.map) return;
    if (changes['center']) {
      this.map.setView([this.center.lat, this.center.lng], this.zoom);
    }
    if (changes['markers']) {
      this.renderMarkers();
    }
  }

  ngOnDestroy(): void {
    this.resizeObserver?.disconnect();
    if (this.map) {
      this.map.remove();
      this.map = null;
    }
  }

  private async initMap(): Promise<void> {
    const L = await import('leaflet');
    this.L = L;

    this.map = L.map(this.mapContainer.nativeElement, {
      center: [this.center.lat, this.center.lng],
      zoom: this.zoom,
      zoomControl: true,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 19,
    }).addTo(this.map);

    this.map.on('click', () => { this.showPopup = false; });

    this.renderMarkers();

    this.resizeObserver = new ResizeObserver(() => {
      if (this.map) this.map.invalidateSize();
    });
    this.resizeObserver.observe(this.mapContainer.nativeElement);
  }

  private renderMarkers(): void {
    if (!this.map || !this.L) return;
    this.leafletMarkers.forEach(m => m.remove());
    this.leafletMarkers = [];

    const icon = this.L.divIcon({
      className: '',
      html: `<div class="pg-marker-pin"></div>`,
      iconSize: [28, 28],
      iconAnchor: [14, 28],
      popupAnchor: [0, -30],
    });

    this.markers.forEach((markerData, index) => {
      const marker = this.L.marker([markerData.lat, markerData.lng], { icon })
        .addTo(this.map);
      marker.on('click', (e: any) => {
        e.originalEvent?.stopPropagation();
        this.openInfoWindow(index, markerData);
      });
      this.leafletMarkers.push(marker);
    });
  }

  openInfoWindow(index: number, markerData: any): void {
    this.activeMarker = markerData;
    this.activePhotoIndex = 0;
    this.selectedPlaceImages = markerData?.place?.photos || markerData?.place?.images || [];
    this.showPopup = true;
  }

  closePopup(): void {
    this.showPopup = false;
    this.activeMarker = null;
  }

  prevPhoto(event: Event): void {
    event.stopPropagation();
    const images = this.selectedPlaceImages;
    if (images.length) {
      this.activePhotoIndex = (this.activePhotoIndex - 1 + images.length) % images.length;
    }
  }

  nextPhoto(event: Event): void {
    event.stopPropagation();
    const images = this.selectedPlaceImages;
    if (images.length) {
      this.activePhotoIndex = (this.activePhotoIndex + 1) % images.length;
    }
  }

  getPhotoUrl(photo: any): string {
    if (photo?.name && this.googlePlacesApiKey) {
      return `https://places.googleapis.com/v1/${photo.name}/media?maxHeightPx=400&key=${this.googlePlacesApiKey}`;
    }
    if (typeof photo === 'string') {
      if (photo.startsWith('places/') && this.googlePlacesApiKey) {
        return `https://places.googleapis.com/v1/${photo}/media?maxHeightPx=400&key=${this.googlePlacesApiKey}`;
      }
      return photo;
    }
    return 'assets/no-image.png';
  }

  openGoogleMapsPlace(): void {
    const placeId = this.activeMarker?.place?.id || this.activeMarker?.place?.place_id;
    if (placeId) {
      window.open(`https://www.google.com/maps/place/?q=place_id:${placeId}`, '_blank');
    }
  }
}
