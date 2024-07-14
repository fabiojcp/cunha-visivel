/*
  Warnings:

  - You are about to drop the `PdfLinkInvertedIndex` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE `PdfLinkInvertedIndex` DROP FOREIGN KEY `PdfLinkInvertedIndex_invertedIndexId_fkey`;

-- DropForeignKey
ALTER TABLE `PdfLinkInvertedIndex` DROP FOREIGN KEY `PdfLinkInvertedIndex_pdfLinkId_fkey`;

-- DropTable
DROP TABLE `PdfLinkInvertedIndex`;
