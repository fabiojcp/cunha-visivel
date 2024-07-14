/*
  Warnings:

  - The primary key for the `PdfLink` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- DropForeignKey
ALTER TABLE `InvertedIndex` DROP FOREIGN KEY `InvertedIndex_pdfLinkId_fkey`;

-- DropForeignKey
ALTER TABLE `Page` DROP FOREIGN KEY `Page_pdfLinkId_fkey`;

-- AlterTable
ALTER TABLE `InvertedIndex` MODIFY `pdfLinkId` VARCHAR(191) NOT NULL;

-- AlterTable
ALTER TABLE `Page` MODIFY `pdfLinkId` VARCHAR(191) NOT NULL;

-- AlterTable
ALTER TABLE `PdfLink` DROP PRIMARY KEY,
    MODIFY `id` VARCHAR(191) NOT NULL,
    ADD PRIMARY KEY (`id`);

-- AddForeignKey
ALTER TABLE `Page` ADD CONSTRAINT `Page_pdfLinkId_fkey` FOREIGN KEY (`pdfLinkId`) REFERENCES `PdfLink`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `InvertedIndex` ADD CONSTRAINT `InvertedIndex_pdfLinkId_fkey` FOREIGN KEY (`pdfLinkId`) REFERENCES `PdfLink`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
