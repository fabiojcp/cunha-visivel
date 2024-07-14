/*
  Warnings:

  - You are about to alter the column `pdfLinkId` on the `InvertedIndex` table. The data in that column could be lost. The data in that column will be cast from `VarChar(191)` to `Int`.
  - You are about to alter the column `pdfLinkId` on the `Page` table. The data in that column could be lost. The data in that column will be cast from `VarChar(191)` to `Int`.
  - The primary key for the `PdfLink` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `metadataId` on the `PdfLink` table. All the data in the column will be lost.
  - You are about to alter the column `id` on the `PdfLink` table. The data in that column could be lost. The data in that column will be cast from `VarChar(191)` to `Int`.
  - Added the required column `pageNumber` to the `InvertedIndex` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE `InvertedIndex` DROP FOREIGN KEY `InvertedIndex_pdfLinkId_fkey`;

-- DropForeignKey
ALTER TABLE `Page` DROP FOREIGN KEY `Page_pdfLinkId_fkey`;

-- DropIndex
DROP INDEX `PdfLink_metadataId_fkey` ON `PdfLink`;

-- AlterTable
ALTER TABLE `InvertedIndex` ADD COLUMN `pageNumber` INTEGER NOT NULL,
    MODIFY `pdfLinkId` INTEGER NOT NULL;

-- AlterTable
ALTER TABLE `Page` MODIFY `pdfLinkId` INTEGER NOT NULL;

-- AlterTable
ALTER TABLE `PdfLink` DROP PRIMARY KEY,
    DROP COLUMN `metadataId`,
    MODIFY `id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD PRIMARY KEY (`id`);

-- AddForeignKey
ALTER TABLE `Page` ADD CONSTRAINT `Page_pdfLinkId_fkey` FOREIGN KEY (`pdfLinkId`) REFERENCES `PdfLink`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `InvertedIndex` ADD CONSTRAINT `InvertedIndex_pdfLinkId_fkey` FOREIGN KEY (`pdfLinkId`) REFERENCES `PdfLink`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
