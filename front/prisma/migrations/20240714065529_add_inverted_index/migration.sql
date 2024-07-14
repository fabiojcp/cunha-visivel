/*
  Warnings:

  - The primary key for the `Page` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `date` on the `Page` table. All the data in the column will be lost.
  - You are about to drop the column `edition` on the `Page` table. All the data in the column will be lost.
  - You are about to drop the column `name` on the `Page` table. All the data in the column will be lost.
  - You are about to drop the column `year` on the `Page` table. All the data in the column will be lost.
  - The primary key for the `PdfLink` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the `Metadata` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE `Page` DROP FOREIGN KEY `Page_pdfLinkId_fkey`;

-- DropForeignKey
ALTER TABLE `PdfLink` DROP FOREIGN KEY `PdfLink_metadataId_fkey`;

-- AlterTable
ALTER TABLE `Page` DROP PRIMARY KEY,
    DROP COLUMN `date`,
    DROP COLUMN `edition`,
    DROP COLUMN `name`,
    DROP COLUMN `year`,
    MODIFY `id` VARCHAR(191) NOT NULL,
    MODIFY `text` LONGTEXT NOT NULL,
    MODIFY `pdfLinkId` VARCHAR(191) NOT NULL,
    ADD PRIMARY KEY (`id`);

-- AlterTable
ALTER TABLE `PdfLink` DROP PRIMARY KEY,
    ADD COLUMN `date` VARCHAR(191) NULL,
    ADD COLUMN `edition` VARCHAR(191) NULL,
    ADD COLUMN `name` VARCHAR(191) NULL,
    ADD COLUMN `year` VARCHAR(191) NULL,
    MODIFY `id` VARCHAR(191) NOT NULL,
    ADD PRIMARY KEY (`id`);

-- DropTable
DROP TABLE `Metadata`;

-- CreateTable
CREATE TABLE `InvertedIndex` (
    `id` VARCHAR(191) NOT NULL,
    `word` VARCHAR(191) NOT NULL,
    `pageId` VARCHAR(191) NOT NULL,
    `pdfLinkId` VARCHAR(191) NOT NULL,

    INDEX `InvertedIndex_word_idx`(`word`),
    INDEX `InvertedIndex_pageId_idx`(`pageId`),
    INDEX `InvertedIndex_pdfLinkId_idx`(`pdfLinkId`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `Page` ADD CONSTRAINT `Page_pdfLinkId_fkey` FOREIGN KEY (`pdfLinkId`) REFERENCES `PdfLink`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `InvertedIndex` ADD CONSTRAINT `InvertedIndex_pageId_fkey` FOREIGN KEY (`pageId`) REFERENCES `Page`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `InvertedIndex` ADD CONSTRAINT `InvertedIndex_pdfLinkId_fkey` FOREIGN KEY (`pdfLinkId`) REFERENCES `PdfLink`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
