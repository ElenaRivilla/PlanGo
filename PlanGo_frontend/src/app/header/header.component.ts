import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { CommonModule } from '@angular/common';
import { UserService } from '../core/services/user.service';
import { ItinerariesService } from '../core/services/itineraries.service';
import { getAuth, signOut } from 'firebase/auth';
import { AuthService } from '../auth/auth.service';
import { BaseToastService } from '../core/services/base-toast.service';
import { ToastModule } from 'primeng/toast';


@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    CommonModule,
    ToastModule,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css',
  animations: [
    trigger('hoverAnimation', [
      state('default', style({ transform: 'scale(1)' })),
      state('hover', style({ transform: 'scale(1.2)' })),
      transition('default <=> hover', animate('300ms ease-in-out')),
    ]),
    trigger('expandHeader', [
      state('collapsed', style({ width: '4rem' })),
      state('expanded', style({ width: '18rem' })),
      transition('collapsed <=> expanded', animate('300ms cubic-bezier(0.4,0,0.2,1)')),
    ]),
  ],
})
export class HeaderComponent {
  buttonStates: { [key: string]: string } = {
    itineraries: 'default',
    expenses: 'default',
    savedPlaces: 'default',
    profile: 'default',
  };
  headerState: 'collapsed' | 'expanded' = 'collapsed';
  userName: string = '';
  userEmail: string = '';
  userPhoto: string = '';
  itinerariesCount: number = 0;

  constructor(
    private router: Router,
    private userService: UserService,
    private itinerariesService: ItinerariesService,
    public authService: AuthService,
    public toast: BaseToastService,
  ) { }

  ngOnInit() {
    this.itinerariesService.getItineraries().subscribe({
      next: (data: any) => {
        this.itinerariesCount = data.itineraries?.length || 0;
      },
      error: () => {
        this.itinerariesCount = 0;
      }
    });

    this.itinerariesService.getIdUser().subscribe({
        next: (idUser: number | null) => {
          if (idUser === null) {
            this.userName = '';
            this.userEmail = '';
            this.userPhoto = '';
            return;
          }
          this.userService.getUserById(idUser)
            .subscribe(userData => {
              this.userName = `${userData.first_name} ${userData.last_name}`;
              this.userEmail = userData.email;
              this.userPhoto = userData.user_image;
            });
        },
        error: () => {
          this.toast.showErrorToast('Error al obtener la información del usuario', false);
        }
      });
  }

  onResetPassword() {
    let email = this.userEmail || prompt('Introduce tu email para restablecer la contraseña:');
    if (email) {
      this.authService.resetPassword(email)
        .then(() => this.toast.showSuccessToast('Se ha enviado un correo para restablecer la contraseña', false))
        .catch(err => this.toast.showErrorToast('Error al enviar el correo', false));
    }
  }

  toggleHeaderWidth() {
    this.headerState = this.headerState === 'collapsed' ? 'expanded' : 'collapsed';
  }

  setHoverState(button: string, state: string): void {
    this.buttonStates[button] = state;
  }

  goToExpense() {
    this.router.navigate(["/expenses"]);
  }

  goToItineraries() {
    this.router.navigate(["/itineraries"])
  }

  goToSavedPlaces() {
    this.router.navigate(['/saved/places']);
  }
}
