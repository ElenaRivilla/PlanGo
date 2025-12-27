import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Auth, createUserWithEmailAndPassword } from '@angular/fire/auth';
import { Router } from '@angular/router';
import { RegisterService } from '../../core/services/register.service';
import { AnimatedBackgroundComponent } from '../../core/animated-background/animated-background.component';
import { ValidatorMessages } from '../../core/validators/validator-messages';

@Component({
  standalone: true,
  selector: 'app-register',
  imports: [CommonModule, FormsModule, HttpClientModule, AnimatedBackgroundComponent],
  templateUrl: './register.component.html',
})
export class RegisterComponent {
  email = '';
  firstName = '';
  lastName = '';
  password = '';
  repeatPassword = '';
  errorMessage = '';
  errorMessageE = '';
  errorMessageN = '';
  errorMessageLN = '';
  errorMessageP = '';
  errorMessageRP = '';
  showPassword = false;
  showRepeatPassword = false;

  constructor(private auth: Auth, private router: Router, private registerService: RegisterService) {}

  clearError(field: string) {
    switch (field) {
      case 'email':
        this.errorMessageE = '';
        break;
      case 'firstName':
        this.errorMessageN = '';
        break;
      case 'lastName':
        this.errorMessageLN = '';
        break;
      case 'password':
        this.errorMessageP = '';
        break;
      case 'repeat-password':
      case 'repeatPassword':
        this.errorMessageRP = '';
        break;
    }
  }
  async register() {

    this.errorMessageE = '';
    this.errorMessageN = '';
    this.errorMessageLN = '';
    this.errorMessageP = '';
    this.errorMessageRP = '';

    let valid = true;

    if (!this.email) {
      this.errorMessageE = ValidatorMessages['invalidEmail'];
      valid = false;
    }
    

    if (!this.firstName) {
      this.errorMessageN = ValidatorMessages['emptyName'];
      valid = false;
    }

    if (!this.lastName) {
      this.errorMessageLN = ValidatorMessages['emptyLastName'];
      valid = false;
    }

    if (!this.password) {
      this.errorMessageP = ValidatorMessages['passwordRequired'];
      valid = false;
    } else if (((this.password.length || this.repeatPassword.length) < 6 || (this.password.length < 6))) {
      this.errorMessageP = ValidatorMessages['wrongPassword'];
      valid = false;
    }  
    
    if (!this.repeatPassword) {
      this.errorMessageRP = ValidatorMessages['passwordRequired'];
      valid = false;
    } else if (this.password !== this.repeatPassword) {
      this.errorMessageRP = ValidatorMessages['wrongRepPassword'];
      valid = false;
    }

    if (!valid) {
      return;
    }

    try {
      const userCredential = await createUserWithEmailAndPassword(this.auth, this.email, this.password);
      const firebaseUser = userCredential.user;
      const idToken = await firebaseUser.getIdToken(); // Obtén el token de Firebase

      const payload = {
        email: this.email,
        first_name: this.firstName,
        last_name: this.lastName,
        username: `${this.firstName[0].toLowerCase()}${this.lastName.split(' ')[0].toLowerCase()}`, // Generar username
        firebase_uid: firebaseUser.uid
      };

      this.registerService.registerUser(idToken, payload).subscribe({
        next: (rs) => {
          this.router.navigate(['/login']);
        },
        error: (err) => {
          console.error('Error al registrar usuario en Django:', err);
          this.errorMessage = 'Error al registrar usuario. Inténtalo de nuevo.';
        },
      });
    } catch (err: any) {
      if (err.code === 'auth/email-already-in-use') {
        this.errorMessageE = ValidatorMessages['existantEmail'];
      }
      console.error('Error al registrar usuario en Firebase:', err);
      this.errorMessage = err.message;
    }
  }

  navigateToLogin() {
    this.router.navigate(['/login']);
  }

  toggleShowPassword(): void {
    this.showPassword = !this.showPassword;
  }

  toggleShowRepeatPassword(): void {
    this.showRepeatPassword = !this.showRepeatPassword;
  }
}