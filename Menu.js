function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'es',  // Idioma original de la página (español)
        includedLanguages: 'en',  // Idioma de destino (inglés)
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE
    }, 'google_translate_element');
}