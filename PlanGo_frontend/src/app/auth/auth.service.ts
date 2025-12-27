import { Injectable } from '@angular/core';
import {  signOut, sendPasswordResetEmail } from 'firebase/auth';
import { Auth } from '@angular/fire/auth';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(
     private auth: Auth,
     private router: Router
    ) {}

  logout() {
    signOut(this.auth).then(() => {
      localStorage.clear();
      this.router.navigate(['/login']);
    });
  }

  resetPassword(email: string): Promise<void> {
    return sendPasswordResetEmail(this.auth, email);
  }
}