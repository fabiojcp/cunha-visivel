/*
  Warnings:

  - You are about to drop the column `pageId` on the `InvertedIndex` table. All the data in the column will be lost.
  - You are about to drop the column `pageNumber` on the `InvertedIndex` table. All the data in the column will be lost.
  - You are about to drop the column `pdfLinkId` on the `InvertedIndex` table. All the data in the column will be lost.

*/
-- DropForeignKey
ALTER TABLE `InvertedIndex` DROP FOREIGN KEY `InvertedIndex_pageId_fkey`;

-- DropForeignKey
ALTER TABLE `InvertedIndex` DROP FOREIGN KEY `InvertedIndex_pdfLinkId_fkey`;

-- AlterTable
ALTER TABLE `InvertedIndex` DROP COLUMN `pageId`,
    DROP COLUMN `pageNumber`,
    DROP COLUMN `pdfLinkId`;

-- CreateTable
CREATE TABLE `PdfLinkInvertedIndex` (
    `pdfLinkId` VARCHAR(191) NOT NULL,
    `invertedIndexId` VARCHAR(191) NOT NULL,

    PRIMARY KEY (`pdfLinkId`, `invertedIndexId`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `PageInvertedIndex` (
    `pageId` VARCHAR(191) NOT NULL,
    `invertedIndexId` VARCHAR(191) NOT NULL,

    PRIMARY KEY (`pageId`, `invertedIndexId`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `PdfLinkInvertedIndex` ADD CONSTRAINT `PdfLinkInvertedIndex_pdfLinkId_fkey` FOREIGN KEY (`pdfLinkId`) REFERENCES `PdfLink`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `PdfLinkInvertedIndex` ADD CONSTRAINT `PdfLinkInvertedIndex_invertedIndexId_fkey` FOREIGN KEY (`invertedIndexId`) REFERENCES `InvertedIndex`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `PageInvertedIndex` ADD CONSTRAINT `PageInvertedIndex_pageId_fkey` FOREIGN KEY (`pageId`) REFERENCES `Page`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `PageInvertedIndex` ADD CONSTRAINT `PageInvertedIndex_invertedIndexId_fkey` FOREIGN KEY (`invertedIndexId`) REFERENCES `InvertedIndex`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
