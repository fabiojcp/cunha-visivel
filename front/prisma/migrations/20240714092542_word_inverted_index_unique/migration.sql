/*
  Warnings:

  - A unique constraint covering the columns `[word]` on the table `InvertedIndex` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX `InvertedIndex_word_key` ON `InvertedIndex`(`word`);
