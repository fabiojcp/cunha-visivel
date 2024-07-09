const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();
const fs = require('fs');
const path = require('path');

// Caminho para o arquivo db.json
const jsonFilePath = path.join(__dirname, 'db.json');

// Ler o arquivo db.json
const jsonData = JSON.parse(fs.readFileSync(jsonFilePath, 'utf-8'));

async function main() {
  const metadata = await prisma.metadata.create({
    data: {
      createdAt: new Date(jsonData.created_at),
      updatedAt: new Date(jsonData.updated_at),
      pdfLinks: {
        create: Object.entries(jsonData.pdf_links).map(([url, pdfLink]) => ({
          url,
          hashSha512: pdfLink.hash_sha512,
          path: pdfLink.path,
          name: pdfLink.name,
          date: pdfLink.date,
          year: pdfLink.year,
          edition: pdfLink.edition,
          pages: {
            create: pdfLink.pages.map(page => ({
              number: page.number,
              text: page.text,
            }))
          }
        }))
      }
    }
  });

  console.log(metadata);
}

main()
  .catch(e => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
