import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CounterDatesComponent } from './counter-dates.component';

describe('CounterDatesComponent', () => {
  let component: CounterDatesComponent;
  let fixture: ComponentFixture<CounterDatesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CounterDatesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CounterDatesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
