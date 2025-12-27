// MENSAJES DE ERROR REUTILIZABLES PARA MOSTRAR EN 
// LOS FORMULARIOS POR EJEMPLO (EL TIPO DE MENSAJE A MANDAR)

// CREATE EXPENSE.
export const ValidatorMessages: { [key: string]: string } = {
    itineraryRequired: 'Debe añadir el itinerario.',
    destinationRequired: 'Debe añadir el destino.',
    payerRequired: 'Debe añadir el pagador.',
    payerAmountRequired: 'Debe añadir un valor mayor a 0',
    debtorsExceedTotal: 'La suma del importe del deudor no puede superar el total pagado.',
    debtorsAmountRequired: 'Debe añadir un valor mayor a 0',
    debtorsSelectRequired: 'Este campo no puede estar vacío.',
    itineraryendDateAfterstartDate: 'La fecha de fin no puede ser anterior a la fecha de inicio.',
    itineraryDatesRequired: 'Selecciona ambas fechas',
    wrongCredentials: 'El email o la contraseña no son correctos.',
    invalidEmail: 'El email no es válido.',
    existantEmail: 'Este email ya está en uso.',
    emptyName: 'El nombre es obligatorio.',
    emptyLastName: 'El apellido es obligatorio',
    passwordRequired: 'La contraseña es obligatoria.',
    wrongRepPassword: 'Las contraseñas no coinciden.',
    wrongPassword: 'La contraseña debe tener al menos 6 carácteres.',
    participantDuplicate: 'Ya existe un participante con ese nombre en este destino.',
    participantAddError: 'Algo falló, no se han creado los participantes.',
    participantEmpty: 'Debes introducir un participante',
    destinationDuplicate: 'Ya existe un destino con ese nombre en este itinerario.',
    destinationsNew: 'No hay destinos creados. ¡Añade el primero!',
    maxDestinations: 'Se ha alcanzado el máximo de destinos por días de itinerario',
};


