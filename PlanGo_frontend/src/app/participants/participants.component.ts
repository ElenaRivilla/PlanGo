import { Component, Input } from '@angular/core';
import { ItinerariesService } from '../core/services/itineraries.service';
import { ParticipantsService } from '../core/services/participants.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HeaderComponent } from '../header/header.component';
import { BaseToastService } from '../core/services/base-toast.service';
import { ToastModule } from 'primeng/toast';
import { trigger, transition, style, animate } from '@angular/animations';
import { ValidatorMessages } from '../core/validators/validator-messages';

@Component({
  selector: 'app-participants-form',
  standalone: true,
  templateUrl: './participants.component.html',
  styleUrl: './participants.component.css',
  imports: [
    CommonModule,
    FormsModule,
    HeaderComponent,
    ToastModule
  ],
  animations: [
    trigger('slideInRight', [
      transition(':enter', [
        style({ transform: 'translateX(100%)', opacity: 0 }),
        animate('300ms ease', style({ transform: 'translateX(0)', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('300ms ease', style({ transform: 'translateX(100%)', opacity: 0 }))
      ])
    ])
  ]
})
export class ParticipantsComponent {
  @Input() destination!: number | null;
  participants: { participant_name: string }[] = [];
  participantName: string = '';
  errorMessage: string = '';
  showInput = false;
  ValidatorMessages = ValidatorMessages;
  formSubmitted = false;

  constructor(
    private itinerariesService: ItinerariesService,
    private participantService: ParticipantsService,
    private toast: BaseToastService
  ) { }

  ngOnInit(): void {
    this.loadParticipants();
  }

  addParticipant(): void {
    let participant = {
      participant_name: this.participantName,
      destination: this.destination,
    };

    this.participantService.createParticipant(participant).subscribe({
      next: () => {
        this.toast.showSuccessToast('Se han añadido el participante', false);
        this.loadParticipants();
        this.showInput = false;
        this.participantName = '';
      },
      error: (err) => {
        this.errorMessage = ValidatorMessages['participantAddError'];
        console.error('Error al crear participante:', err);
      },
    });
  }

  loadParticipants(): void {
    if (!this.destination) return;
    this.participantService.getParticipantsByDestination(this.destination).subscribe({
      next: (data: any) => {
        this.participants = Array.isArray(data.Participants) ? data.Participants : [];
      },
      error: () => {
        this.participants = [];
      }
    });
  }

  addParticipantWithDetails(participantName: string, destinationId: number): void {
  this.formSubmitted = true;

  if (!participantName || participantName.trim() === '') {
    this.errorMessage = ValidatorMessages['participantEmpty'];
    return;
  }

  let normalizedName = participantName.trim().toLowerCase();
  let exists = this.participants.some(
    p => p.participant_name.trim().toLowerCase() === normalizedName
  );
  if (exists) {
    this.errorMessage = ValidatorMessages['participantDuplicate'];
    return;
  }

  this.errorMessage = '';
  this.participantName = participantName;
  this.destination = destinationId;
  this.addParticipant();
}

  participantExists(): boolean {
    let normalizedName = this.participantName.trim().toLowerCase();
    return this.participants.some(
      p => p.participant_name.trim().toLowerCase() === normalizedName
    );
  }

  cancelAdd() {
    this.showInput = false;
    this.participantName = '';
    this.errorMessage = '';
  } 
}
