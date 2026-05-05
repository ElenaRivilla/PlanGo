import { Injectable } from '@angular/core';
import { signOut, sendPasswordResetEmail } from 'firebase/auth';
import { Auth } from '@angular/fire/auth';
import { Router } from '@angular/router';
import { ItinerariesService } from '../core/services/itineraries.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(
    private auth: Auth,
    private router: Router,
    private itinerariesService: ItinerariesService,
  ) {}

  logout() {
    signOut(this.auth).then(() => {
      this.itinerariesService.invalidateUser();
      localStorage.clear();
      this.router.navigate(['/login']);
    });
  }

  resetPassword(email: string): Promise<void> {
    return sendPasswordResetEmail(this.auth, email);
  }
}