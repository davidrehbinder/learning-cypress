describe('Learning Cypress, one test at a time.', () => {
    it('Visit the kitchen sink.', () => {
        cy.visit('https://example.cypress.io')
        cy.contains('type')
    })
})