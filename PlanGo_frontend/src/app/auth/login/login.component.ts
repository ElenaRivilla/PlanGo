import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { Auth, signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from '@angular/fire/auth';
import { Router } from '@angular/router';
import { LoginService } from '../../core/services/login.service'; // Importa el servicio
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { globals } from '../../core/globals';
import { AnimatedBackgroundComponent } from '../../core/animated-background/animated-background.component';
import { ValidatorMessages } from '../../core/validators/validator-messages';

@Component({
  standalone: true,
  selector: 'app-login',
  imports: [FormsModule, CommonModule, AnimatedBackgroundComponent],
  templateUrl: './login.component.html',
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class LoginComponent {
  errorMessage = '';
  errorMessageE = '';
  errorMessageP = '';
  errorMessageG = '';
  email = '';
  password = '';
  showPassword = false;

  constructor(
    private auth: Auth,
    private router: Router,
    private loginService: LoginService,
  ) { }

  async loginWithGoogle() {
    try {
      let provider = new GoogleAuthProvider();
      let result = await signInWithPopup(this.auth, provider);
      let firebaseUser = result.user;
      let idToken = await firebaseUser.getIdToken();

      localStorage.setItem('authToken', idToken);

      this.loginService.loginWithGoogle(idToken).subscribe({
        next: () => {
          this.router.navigate(['/itineraries']);
        },
        error: (err) => {
          console.error('Error al autenticar usuario en el backend:', err);
          this.errorMessage = 'Error al autenticar usuario. Inténtalo de nuevo.';
        },
      });
    } catch (error: any) {
      console.error('Error al iniciar sesión con Google:', error);
      this.errorMessage = error.message;
    }
  }

  async login() {
    this.errorMessage = '';
    this.errorMessageE = '';
    this.errorMessageP = '';
    this.errorMessageG = '';
    
    try {
      let result = await signInWithEmailAndPassword(this.auth, this.email, this.password);
      let firebaseUser = result.user;
      let idToken = await firebaseUser.getIdToken();

      // Guarda el token en localStorage
      localStorage.setItem(globals.keys.accessToken, idToken);

      // Llama al servicio para autenticar con el backend
      this.loginService.loginWithEmail(idToken).subscribe({
        next: () => {
          this.router.navigate(['/itineraries']);
        },
        error: (err) => {
          console.error('Error al autenticar usuario en el backend:', err);
          this.errorMessage = 'Error al autenticar usuario. Inténtalo de nuevo.';
        },
      });
    } catch (error: any) {
      if (error.code === 'auth/invalid-email') {
        this.errorMessageE = ValidatorMessages['invalidEmail'];
      } else if (error.code === 'auth/wrong-password' || error.code === 'auth/missing-password') {
        this.errorMessageP = ValidatorMessages['passwordRequired'];
      } else if (
        error.code === 'auth/invalid-login-credentials' ||
        error.code === 'auth/user-mismatch' ||
        error.code === 'auth/invalid-credential'
      ) {
        this.errorMessageG = ValidatorMessages['wrongCredentials'];
      }
      console.error('Error al iniciar sesión:', error);
    }
  }

  navigateToRegister() {
    this.router.navigate(['/register']);
  }

  toggleShowPassword(): void {
    this.showPassword = !this.showPassword;
  }
}