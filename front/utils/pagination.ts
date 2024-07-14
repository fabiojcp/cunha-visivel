export function paginateResults<T>(
    results: T[],
    page: number,
    resultsPerPage: number
  ): { paginatedResults: T[]; total: number; totalPages: number; currentPage: number } {
    const total = results.length;
    const totalPages = Math.ceil(total / resultsPerPage);
    const paginatedResults = results.slice((page - 1) * resultsPerPage, page * resultsPerPage);
  
    return {
      paginatedResults,
      total,
      totalPages,
      currentPage: page,
    };
  }
  