import { Component, Input, OnInit, CUSTOM_ELEMENTS_SCHEMA, ViewChildren, QueryList } from '@angular/core';
import { GoogleMapsModule } from '@angular/google-maps';
import { CommonModule } from '@angular/common';
import { ViewChild } from '@angular/core';
import { MapInfoWindow, MapMarker } from '@angular/google-maps';
import { ApiKeyService } from '../core/services/api-key.service';
import { TooltipModule } from 'primeng/tooltip';
import { SearchPlacesService } from '../core/services/search-places.service';

@Component({
  standalone: true,
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css'],
  imports: [
    CommonModule,
    GoogleMapsModule,
    TooltipModule
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class MapComponent implements OnInit {
  @ViewChild(MapInfoWindow) infoWindow!: MapInfoWindow;
  @ViewChildren(MapMarker) markerRefs!: QueryList<MapMarker>;
  @Input() center = { lat: 39.720007, lng: 2.910419 };
  @Input() zoom = 13; // Default zoom level
  @Input() mapOptions: google.maps.MapOptions = {
    mapId: 'DEMO_MAP_ID',
    disableDefaultUI: true,
  };
  @Input() markers: { lat: number, lng: number, label?: string, place?: any }[] = [];
  @Input() selectedPlace: any = null;
  activeMarker: any = null;
  activePhotoIndex: number = 0;
  selectedPlaceImages: any[] = [];
  googlePlacesApiKey?: string;

  constructor(
    public apiKeyService: ApiKeyService,
  ) { }

  ngOnInit(): void {
    this.apiKeyService.getGooglePlacesApiKey().subscribe({
      next: (data: any) => {
        this.googlePlacesApiKey = data.googlePlacesApiKey;
      },
      error: (err: any) => {
        console.log("No ha recibido la KEY de Google Places API.")
      }
    });
  }

  openInfoWindow(index: number, markerData: any) {
    this.activeMarker = markerData;
    this.activePhotoIndex = 0;
    this.selectedPlaceImages = markerData?.place?.photos || markerData?.place?.images || [];
    const marker = this.markerRefs.get(index);
    if (marker) {
      this.infoWindow.open(marker);
    }
  }

  prevPhoto(event: Event) {
    event.stopPropagation();
    const images = this.selectedPlaceImages;
    if (images.length) {
      this.activePhotoIndex = (this.activePhotoIndex - 1 + images.length) % images.length;
    }
  }

  nextPhoto(event: Event) {
    event.stopPropagation();
    const images = this.selectedPlaceImages;
    if (images.length) {
      this.activePhotoIndex = (this.activePhotoIndex + 1) % images.length;
    }
  }

  getPhotoUrl(photo: any): string {
    // Si es Google Place Photo (objeto con .name)
    if (photo?.name && this.googlePlacesApiKey) {
      return `https://places.googleapis.com/v1/${photo.name}/media?maxHeightPx=400&key=${this.googlePlacesApiKey}`;
    }
    // Si es string y parece una ruta de Google Places
    if (typeof photo === 'string') {
      if (photo.startsWith('places/') && this.googlePlacesApiKey) {
        return `https://places.googleapis.com/v1/${photo}/media?maxHeightPx=400&key=${this.googlePlacesApiKey}`;
      }
      // Si es una URL absoluta o relativa a tu servidor
      return photo;
    }
    return 'assets/no-image.png';
  }

  openGoogleMapsPlace(): void {
    let placeId = this.activeMarker?.place?.id || this.activeMarker?.place?.place_id;
    if (placeId) {
      window.open(`https://www.google.com/maps/place/?q=place_id:${placeId}`, '_blank');
    }
  }
}