import { Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { ItinerariesComponent } from './itineraries/itineraries.component';
import { DestinationsComponent} from './destinations/destinations.component';
import { ExpensesComponent } from './expenses/expenses.component';
import { ParticipantsComponent } from './participants/participants.component';
import { SearchLocationsComponent } from './search-locations/search-locations.component';
import { SearchPlacesComponent } from './search-places/search-places.component';
import { SavedPlacesComponent } from './saved-places/saved-places.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent, data: { animation: 'LoginPage' } },
  { path: 'register', component: RegisterComponent, data: { animation: 'RegisterPage' } },
  { path: 'itineraries', component: ItinerariesComponent },
  { path: 'participants', component: ParticipantsComponent },
  { path: 'destinations/:itineraryId', component: DestinationsComponent },
  { path: 'search/places/:itineraryId', component: SearchLocationsComponent },
  { path: 'search/places', component: SearchPlacesComponent },
  { path: 'saved/places', component: SavedPlacesComponent },
  { path: 'expenses', component: ExpensesComponent },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: 'login' },
];