// VALIDADORES PERSONALIZADOS (QUE QUEREMOS QUE HAYA EN LOS INPUTS (LA LÓGICA))
import { AbstractControl, ValidationErrors, ValidatorFn, FormGroup } from '@angular/forms';

export class CustomValidators {
    addDebtorError: string = '';
    
    static payerAndAmountRequired(): ValidatorFn {
        return (form: AbstractControl): ValidationErrors | null => {
        let group = form as FormGroup;
        let payer = group.get('payer')?.value;
        let totalAmount = Number(group.get('total_amount')?.value);

        let errors: ValidationErrors = {};

        if (!payer) errors['payerRequired'] = true;
        // Solo muestra payerAmountRequired si hay pagador seleccionado
        if (payer && (!totalAmount || totalAmount <= 0)) errors['payerAmountRequired'] = true;

        return Object.keys(errors).length ? errors : null;
        }
    }

    static debtorsNotExceedTotalAmount(): ValidatorFn {
        return (form: AbstractControl): ValidationErrors | null => {
            let group = form as FormGroup;
            let totalAmount = Number(group.get('total_amount')?.value);
            let debtors = group.get('debtors')?.value || [];
            let debtorsTotal = debtors.reduce(
            (sum: number, debtor: any) => sum + Number(debtor.amount || 0), 0
            );
            return debtorsTotal > totalAmount ? { debtorsExceedTotal: true } : null;
        };
    }

    static itineraryAndDestinationRequired(): ValidatorFn {
        return (form: AbstractControl): ValidationErrors | null => {
            let group = form as FormGroup;
            let itinerary = group.get('itinerary')?.value;
            let destination = group.get('destination')?.value;
            let errors: ValidationErrors = {};
            if (!itinerary) {
                errors['itineraryRequired'] = true;
            }
            if (!destination) {
                errors['destinationRequired'] = true;
            }
            return Object.keys(errors).length ? errors : null; 
        }
    }

    static debtorsAmountRequiredPersonalized(): ValidatorFn {
        return (form: AbstractControl): ValidationErrors | null => {
            let group = form as FormGroup;
            let typeExpense = group.get('type_expense')?.value;
            let debtors = group.get('debtors')?.value || [];
            let hasDebtorAmount = debtors.some((debtor: any) => Number(debtor.amount) > 0);
            let errors: ValidationErrors = {};
            if (typeExpense === 'Personalized' && debtors.length > 0 && !hasDebtorAmount) errors['debtorsAmountRequired'] = true;
            return Object.keys(errors).length ? errors : null;
        }
    }

    static debtorsSelectRequired(): ValidatorFn {
        return (form: AbstractControl): ValidationErrors | null => {
            let group = form as FormGroup;
            let debtors = group.get('debtors')?.value || [];
            let noDebtorSelected = debtors.some((debtor: any) => !debtor.id);
            let errors: ValidationErrors = {};
            if (noDebtorSelected) errors['debtorsSelectRequired'] = true;
            return Object.keys(errors).length ? errors : null;
        }
    }

    static endDateAfterStartDate(): ValidatorFn {
        return (group: AbstractControl): ValidationErrors | null => {
            let form = group as FormGroup;
            let start = form.get('startDate')?.value;
            let end = form.get('endDate')?.value;
            if (start && end && new Date(end) < new Date(start)) return { endDateBeforeStartDate: true };
            return null;
        };
    }
}

