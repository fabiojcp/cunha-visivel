-- CreateTable
CREATE TABLE `PdfLinkInvertedIndex` (
    `pdfLinkId` VARCHAR(191) NOT NULL,
    `invertedIndexId` VARCHAR(191) NOT NULL,

    PRIMARY KEY (`pdfLinkId`, `invertedIndexId`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `PdfLinkInvertedIndex` ADD CONSTRAINT `PdfLinkInvertedIndex_pdfLinkId_fkey` FOREIGN KEY (`pdfLinkId`) REFERENCES `PdfLink`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `PdfLinkInvertedIndex` ADD CONSTRAINT `PdfLinkInvertedIndex_invertedIndexId_fkey` FOREIGN KEY (`invertedIndexId`) REFERENCES `InvertedIndex`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
