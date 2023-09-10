# LLM Exploration for Mayor's Office Of New Urban Mechanics

## Background

The Mayor's Office of New Urban Mechanics is focused on creating innovative and equitable services for the residents of Boston.

Project contributors:

[Michael Evans](https://www.boston.gov/departments/new-urban-mechanics/michael-evans)

[Michael McKenna Miller](https://www.linkedin.com/in/mckennamiller/)

[Chirag Mahapatra](https://www.linkedin.com/in/chiragmahapatra/)

The goal of this project was to explore usig LLMs to make generating RFPs easier for Boston government employees.

## What are RFPs?

A request for proposal (RFP) is a business document that announces a project, describes it, and solicits bids from qualified contractors to complete it. Most organizations prefer to launch their projects using RFPs, and many governments always use them.

[Source](https://www.investopedia.com/terms/r/request-for-proposal.asp)

## How we built this?

We take a number of existing RFPs such as 
- 5th Quarter Summer Programming by Boston Public Schools
- Bicycle Repair and Maintenance Employee Benefit by People Operations
- Boston Eats at Open Meal Sites by Mayor’s Office of Food Justice

We use LlamaIndex's vector store index which stores documents as vector indexes. Using a vector store index lets you introduce similarity into your LLM application. This is the best index for when your workflow compares texts for semantic similarity via vector search.

Once we had this, we iterated on generating the RFP based on a number of different prompts.

We tried the following high level experiments:
1. Use one big prompt to create the RFP.
2. Create prompts for each section which are independent of each other. The key sections were Quick Description, Statement of Need, Expectations, and Summary. In addition, the Expectations section was expected to have 4 sections: Materials/Resources, Services, Labor, and Quality.
3. Create prompts in an order which takes in previous responses from the LLM.

Finally, we also iterated on each sub prompt by passing different examples. However, we realized that most of these did not significantly improve the quality of the prompt.

Approach 3 worked the best for our use case. We determined the best approach by relying on Michael's experience with evaluating RFPs.

The final aspect of the project was to build the web app. The goal was to make it really easy for the user to generate a high quality RFP draft which they can use to iterate. 

We built the app on Streamlit. The app is a single page application which shows a number of questions to the user and allows the user to edit the output. Finally, the user can export the draft as a pdf.

Demo: https://www.loom.com/share/a14d17656078410e8720dc79f3c7efab

## Next Steps

- Allow the user to upload documents to fine tune LLMs before generating RFPs.
- Allow the user to export documents to Google Docs
- Allow collaboration while generating and editing docs